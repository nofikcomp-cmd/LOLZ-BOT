from aiogram.fsm.state import State, StatesGroup

class WorkerStates(StatesGroup):
    waiting_for_deals_count = State()
    waiting_for_balance_input = State()
    waiting_for_tag_input = State()
    waiting_for_unfake_deals = State()

class ReqStates(StatesGroup):
    waiting_for_gram = State()
    waiting_for_card = State()
    waiting_for_phone = State()
    waiting_for_usdt = State()