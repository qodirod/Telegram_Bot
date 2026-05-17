from sqlalchemy import select

from app.database.models import async_session, User, Game, Prediction
from app.data.matches import MATCHES


STARTING_BALANCE = 100


# ---------- User management ----------

async def set_user(tg_id: int, username: str | None = None, first_name: str | None = None):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                tg_id=tg_id,
                username=username,
                first_name=first_name,
                language="en",
                total_points=0,
                balance=STARTING_BALANCE
            )
            session.add(user)
            await session.commit()
            return

        updated = False

        if user.username != username:
            user.username = username
            updated = True

        if user.first_name != first_name:
            user.first_name = first_name
            updated = True

        if user.balance is None:
            user.balance = STARTING_BALANCE
            updated = True

        if user.total_points is None:
            user.total_points = 0
            updated = True

        if not user.language:
            user.language = "en"
            updated = True

        if updated:
            await session.commit()


async def get_user_by_tg_id(tg_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        return result.scalar_one_or_none()


async def update_user_language(tg_id: int, language: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        if user:
            user.language = language
            await session.commit()


async def get_user_language(tg_id: int) -> str:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        return user.language if user and user.language else "en"


# ---------- Game seeding ----------

async def seed_games():
    async with async_session() as session:
        existing_games = await session.execute(select(Game))
        existing_games = existing_games.scalars().all()

        existing_by_code = {game.code: game for game in existing_games}

        for code, info in MATCHES.items():
            if code not in existing_by_code:
                session.add(
                    Game(
                        code=code,
                        team1=info["team1"],
                        team2=info["team2"],
                        match_date=info["date"],
                        match_time=info["time"]
                    )
                )
            else:
                game = existing_by_code[code]

                changed = False

                if game.team1 != info["team1"]:
                    game.team1 = info["team1"]
                    changed = True

                if game.team2 != info["team2"]:
                    game.team2 = info["team2"]
                    changed = True

                if game.match_date != info["date"]:
                    game.match_date = info["date"]
                    changed = True

                if game.match_time != info["time"]:
                    game.match_time = info["time"]
                    changed = True

        await session.commit()


async def get_game_by_code(code: str):
    async with async_session() as session:
        result = await session.execute(select(Game).where(Game.code == code))
        return result.scalar_one_or_none()


# ---------- Predictions ----------

async def save_prediction(tg_id: int, game_code: str, selected_team: str) -> str:
    async with async_session() as session:
        existing = await session.execute(
            select(Prediction).where(
                Prediction.user_tg_id == tg_id,
                Prediction.game_code == game_code
            )
        )

        if existing.scalar_one_or_none():
            return "exists"

        prediction = Prediction(
            user_tg_id=tg_id,
            game_code=game_code,
            selected_team=selected_team,
            points=0
        )

        session.add(prediction)
        await session.commit()

        return "saved"


async def get_user_predictions(tg_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Prediction, Game)
            .join(Game, Prediction.game_code == Game.code)
            .where(Prediction.user_tg_id == tg_id)
            .order_by(Game.match_date, Game.match_time)
        )

        return result.all()


# ---------- Results, points, balance ----------

async def set_game_result(code: str, winner: str, result: str) -> bool:
    async with async_session() as session:
        game_result = await session.execute(select(Game).where(Game.code == code))
        game = game_result.scalar_one_or_none()

        if not game:
            return False

        game.winner = winner
        game.result = result

        await session.commit()

    await calculate_points_for_game(code)
    await recalculate_all_users_balance()

    return True


async def calculate_points_for_game(code: str):
    async with async_session() as session:
        game_result = await session.execute(select(Game).where(Game.code == code))
        game = game_result.scalar_one_or_none()

        if not game or not game.winner:
            return

        predictions_result = await session.execute(
            select(Prediction).where(Prediction.game_code == code)
        )
        predictions = predictions_result.scalars().all()

        for prediction in predictions:
            if prediction.selected_team == game.winner:
                prediction.points = 1
            else:
                prediction.points = -1

        await session.commit()


async def recalculate_all_users_balance():
    async with async_session() as session:
        users_result = await session.execute(select(User))
        users = users_result.scalars().all()

        for user in users:
            predictions_result = await session.execute(
                select(Prediction).where(Prediction.user_tg_id == user.tg_id)
            )
            predictions = predictions_result.scalars().all()

            total_points = sum(prediction.points or 0 for prediction in predictions)

            user.total_points = total_points
            user.balance = STARTING_BALANCE + total_points

        await session.commit()


async def get_leaderboard(limit: int = 10):
    async with async_session() as session:
        result = await session.execute(
            select(User)
            .order_by(User.balance.desc(), User.total_points.desc())
            .limit(limit)
        )

        return result.scalars().all()