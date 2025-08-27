from aiogram import Router


from . import common


router = Router()
router.include_router(common.router)