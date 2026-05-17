from sqlalchemy import select, func
from app.database.models import async_session, User, Game, Prediction
from app.data.matches import MATCHES


# ---------- User management ----------
async def set_user(tg_id: int, username: str | None = None, first_name: str | None = None):
    async with async_session() as session:
        user = await session.execute(select(User).where(User.tg_id == tg_id))
        user = user.scalar_one_or_none()
        if not user:
            user = User(tg_id=tg_id, username=username, first_name=first_name)
            session.add(user)
            await session.commit()
        else:
            # update info if changed
            updated = False
            if user.username != username:
                user.username = username
                updated = True
            if user.first_name != first_name:
                user.first_name = first_name
                updated = True
            if updated:
                await session.commit()


async def update_user_language(tg_id: int, language: str):
    async with async_session() as session:
        user = await session.execute(select(User).where(User.tg_id == tg_id))
        user = user.scalar_one_or_none()
        if user:
            user.language = language
            await session.commit()


async def get_user_language(tg_id: int) -> str:
    async with async_session() as session:
        user = await session.execute(select(User).where(User.tg_id == tg_id))
        user = user.scalar_one_or_none()
        return user.language if user else 'en'


# ---------- Game seeding ----------
async def seed_games():
    async with async_session() as session:
        existing_codes = (await session.execute(select(Game.code))).scalars().all()
        for code, info in MATCHES.items():
            if code not in existing_codes:
                session.add(Game(
                    code=code,
                    team1=info['team1'],
                    team2=info['team2'],
                    match_date=info['date'],
                    match_time=info['time']
                ))
        await session.commit()


async def get_game_by_code(code: str):
    async with async_session() as session:
        game = await session.execute(select(Game).where(Game.code == code))
        return game.scalar_one_or_none()


async def save_prediction(tg_id: int, game_code: str, selected_team: str) -> str:
    async with async_session() as session:
        # check existence
        exists = await session.execute(
            select(Prediction).where(
                Prediction.user_tg_id == tg_id,
                Prediction.game_code == game_code
            )
        )
        if exists.scalar_one_or_none():
            return 'exists'

        prediction = Prediction(
            user_tg_id=tg_id,
            game_code=game_code,
            selected_team=selected_team
        )
        session.add(prediction)
        await session.commit()
        return 'saved'


async def get_user_predictions(tg_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Prediction, Game)
            .join(Game, Prediction.game_code == Game.code)
            .where(Prediction.user_tg_id == tg_id)
            .order_by(Game.match_date, Game.match_time)
        )
        return result.all()  # list of tuples (Prediction, Game)


# ---------- Game results & points ----------
async def set_game_result(code: str, winner: str, result: str) -> bool:
    async with async_session() as session:
        game = await session.execute(select(Game).where(Game.code == code))
        game = game.scalar_one_or_none()
        if not game:
            return False
        game.winner = winner
        game.result = result
        await session.commit()
    # Recalculate points for this game and update total user points
    await calculate_points_for_game(code)
    await recalculate_all_users_total()
    return True


async def calculate_points_for_game(code: str):
    async with async_session() as session:
        game = await session.execute(select(Game).where(Game.code == code))
        game = game.scalar_one()
        winner = game.winner
        predictions = await session.execute(select(Prediction).where(Prediction.game_code == code))
        predictions = predictions.scalars().all()
        for pred in predictions:
            pred.points = 1 if pred.selected_team == winner else 0
        await session.commit()


async def recalculate_all_users_total():
    async with async_session() as session:
        users = await session.execute(select(User))
        users = users.scalars().all()
        for user in users:
            total = await session.execute(
                select(func.sum(Prediction.points)).where(Prediction.user_tg_id == user.tg_id)
            )
            total = total.scalar() or 0
            user.total_points = total
        await session.commit()


async def get_leaderboard(limit: int = 10):
    async with async_session() as session:
        result = await session.execute(
            select(User)
            .where(User.total_points > 0)
            .order_by(User.total_points.desc())
            .limit(limit)
        )
        return result.scalars().all()
