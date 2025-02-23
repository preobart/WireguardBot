import sh

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, BufferedInputFile
from aiogram.fsm.context import FSMContext
from keyboards.user_keyboard import create_userlist_keyboard
from filters.is_admin import IsAdmin
from states.user import AddUser
from utils.utils import generate_qr_from_file, is_valid_username, is_username_in_clients, get_next_available_ip
from utils.constants import PATH
from lexicon.lexicon import LEXICON

router = Router()
router.message.filter(IsAdmin())
    
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON["start"])


@router.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON["help"])


@router.message(Command('clients'))
async def process_list_command(message: Message):
    clients = sh.sudo.bash(f"{PATH}wireguard-install.sh", _in="2\n", _err=True)
    await message.answer(LEXICON["clients"].format(clients=clients) if clients else LEXICON[ "no_clients"])


@router.message(Command('create'))
async def process_adduser_command(message: Message, state: FSMContext):
    await message.answer(LEXICON["create_prompt"])
    await state.set_state(AddUser.waiting_for_username)


@router.message(AddUser.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    clients = sh.sudo.bash(f"{PATH}wireguard-install.sh", _in="2\n", _err=True)
    username = message.text.strip()
    ip = get_next_available_ip()
    
    if not is_valid_username(username) or is_username_in_clients(username, clients):
        await message.answer(LEXICON["create_invalid"])
        return  
    
    if not ip:
        await message.answer(LEXICON["no_ip"])
        return

    sh.sudo.bash(f"{PATH}wireguard-install.sh", _in=f"1\n{username}\n{ip}\n{ip}", _err=True, _out=True)

    file_path = f'{PATH}clients/wg0-client-{username}.conf'
    qr = generate_qr_from_file(file_path)
    
    await message.answer_document(FSInputFile(file_path),
        caption=LEXICON["create_success"].format(username=username))
    await message.answer_photo(BufferedInputFile(qr.getvalue(), filename="qr.png"))

    await state.clear()


@router.message(Command('revoke'))
async def process_revokeuser_command(message: Message):
    clients = sh.sudo.bash(f"{PATH}wireguard-install.sh", _in="2\n", _err=True)
    
    if clients:
        await message.answer(LEXICON["revoke_prompt"], 
                             reply_markup=create_userlist_keyboard("revoke", clients.strip().split("\n")))
    else:
        await message.answer(LEXICON["no_clients"])
    
    
@router.callback_query(F.data.startswith("revoke:"))
async def confirm_revoke_user(callback: CallbackQuery):
    usernum, username = callback.data.split(":")[1].strip().split(") ", 1)
    clients = sh.sudo.bash(f"{PATH}wireguard-install.sh", _in="2\n", _err=True)
    
    if not is_username_in_clients(username, clients):
        await callback.message.edit_text(
            text=LEXICON["no_user"].format(username=username), 
            reply_markup=None)
        return
    
    sh.sudo.bash(f"{PATH}wireguard-install.sh", _in=f"3\n{usernum}", _err=True)
    
    await callback.message.edit_text(
        text=LEXICON["revoke_success"].format(username=username), 
        reply_markup=None)


@router.message(Command("config"))
async def process_getconfig_command(message: Message):
    clients = sh.sudo.bash(f"{PATH}wireguard-install.sh", _in="2\n", _err=True)
    if clients:
        await message.answer(LEXICON["config_prompt"], 
                             reply_markup=create_userlist_keyboard("config", clients.strip().split("\n")))
    else:
        await message.answer(LEXICON["no_clients"])


@router.callback_query(F.data.startswith("config:"))
async def confirm_revoke_user(callback: CallbackQuery):
    _, username = callback.data.split(":")[1].strip().split(") ", 1)
    clients = sh.sudo.bash(f"{PATH}wireguard-install.sh", _in="2\n", _err=True)
    
    if not is_username_in_clients(username, clients):
        await callback.message.edit_text(
            LEXICON["no_user"].format(username=username), 
            reply_markup=None)
        return
  
    file_path = f'{PATH}clients/wg0-client-{username}.conf'
    qr = generate_qr_from_file(file_path)

    await callback.message.edit_text(text=LEXICON["config_received"], reply_markup=None)
    await callback.message.answer_document(FSInputFile(file_path))
    await callback.message.answer_photo(BufferedInputFile(qr.getvalue(), filename="qr.png"))
