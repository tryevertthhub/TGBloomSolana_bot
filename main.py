import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from solders.keypair import Keypair
import base58
from datetime import datetime
from pytz import timezone

# Load the .env file
load_dotenv()

# Fetch the bot token from the environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Solana Wallet Generator Class
class SolanaKeyGenerator:
    """Handles the generation and management of Solana keypairs."""

    def __init__(self):
        self.keypair = None

    def generate_new_keypair(self):
        """Generate a new Solana keypair."""
        self.keypair = Keypair()
        return self

    @property
    def public_key(self):
        """Get public key (address) as base58 string."""
        return str(self.keypair.pubkey())

    @property
    def private_key_base58(self):
        """Get private key as base58 string."""
        return base58.b58encode(self.keypair.secret()).decode("ascii")


# Function to generate a new Solana wallet
def generate_solana_wallet():
    """Generate and return a new Solana wallet."""
    generator = SolanaKeyGenerator()
    generator.generate_new_keypair()
    return generator

# Function to get the current US time
def get_us_time():
    """Returns the current time in US Eastern Time Zone."""
    eastern = timezone("US/Eastern")
    now = datetime.now(eastern)
    return now.strftime("%H:%M:%S.%f")[:-3]  # Format: HH:MM:SS.mmm

# DashboardManager: Manages the navigation between different dashboards
class DashboardManager:
    """Manages dashboard UI and navigation."""

    def __init__(self):
        self.wallet_generator = generate_solana_wallet()
        self.current_dashboard = "main"

    async def show_main_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Displays the main dashboard."""
        self.current_dashboard = "main"
        wallet_address = self.wallet_generator.public_key
        # Wallet and Status
        balance = "0 SOL (USD $0)"
        status = "🔴 You currently have no SOL in your wallet.\nTo start trading, please deposit SOL to your address."

        # Buttons for main dashboard
        keyboard = [
            [InlineKeyboardButton("👜Positions", callback_data='positions'), InlineKeyboardButton("🏹LP Sniper", callback_data='lp_sniper')],
            [InlineKeyboardButton("🤖Copy Trade", callback_data='copy_trade'), InlineKeyboardButton("💤AFK Mode", callback_data='afk_mode')],
            [InlineKeyboardButton("Withdraw", callback_data='withdraw'), InlineKeyboardButton("⚙️Settings", callback_data='settings')],
            [InlineKeyboardButton("🚮Close", callback_data='close'), InlineKeyboardButton("♻️Refresh", callback_data='refresh')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        last_updated = get_us_time()
        
        # Main dashboard content
        message = (
            f"Welcome to Bloom! 🌸\n\n"
            f"Let your trading journey *blossom* with us!\n\n"
            f"💜 *Your Solana Wallet Address:*\n"
            f"`{wallet_address}`\n"
            f"*Balance:* {balance}\n\n"
            f"{status}\n\n"
            f"📚 *Resources:*\n"
            f" \n"
            f"[📖 Bloom Guides](https://example.com)\n"
            f"[🔔 Bloom X](https://example.com)\n"
            f"[🌐 Bloom Website](https://example.com)\n"
            f"[💛 Bloom Portal](https://example.com)\n\n"
            f"🕒 Last updated: {last_updated}"
        )

        if update.callback_query:
            # Check if content or markup is different before editing
            if update.callback_query.message.text != message or update.callback_query.message.reply_markup != reply_markup:
                print(" ----------------refresh_mode!-------------------")

                current_time = get_us_time()
                print(current_time)

                await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)
        else:
            await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    async def show_afk_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Displays the AFK Mode (ZFK Mode) dashboard."""
        self.current_dashboard = "afk"

        wallet_address = self.wallet_generator.public_key

        # Buttons for AFK Mode dashboard
        keyboard = [
            [InlineKeyboardButton("Add new config", callback_data='add_config')],
            [InlineKeyboardButton("Pause All", callback_data='pause_all'), InlineKeyboardButton("Start All", callback_data='start_all')],
            [InlineKeyboardButton("Back", callback_data='back'), InlineKeyboardButton("♻️Refresh", callback_data='refresh')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        last_updated = get_us_time()

        # AFK Mode dashboard content
        message = (
            f"🌸 *Bloom AFK*\n\n"
            f"💡 Run your bot while you are away!\n\n"
            f"AFK Wallet:\n"
            f"→ `W1: {wallet_address}`\n\n"
            f"🟢 AFK mode is *active*\n"
            f"🔴 AFK mode is *inactive*\n\n"
            f"⚠️ Please wait 10 seconds after each change for it to take effect.\n\n"
            f"⚠️ Changing your Default wallet? Remember to remake your tasks to use the new wallet for future transactions.\n\n"
            f"🕒 Last updated: {last_updated}"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)

    async def show_settings_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Displays the settings dashboard."""
        self.current_dashboard = "setting"

        # Buttons for settings dashboard
        keyboard = [
            [InlineKeyboardButton("Fee", callback_data='feesetting'), InlineKeyboardButton("💰Wallet", callback_data='wallet')],
            [InlineKeyboardButton("Buy Presets", callback_data='buy_presets'), InlineKeyboardButton("Sell Presets", callback_data='sell_presets')],
            [InlineKeyboardButton("Spot Presets", callback_data='spot_presets'), InlineKeyboardButton("Sniper Presets", callback_data='sniper_presets')],
            [InlineKeyboardButton("Degen Mode", callback_data='degen_mode'), InlineKeyboardButton("MEV Protect", callback_data='mev_protect')],
            [InlineKeyboardButton("Buy: node", callback_data='buy_node'), InlineKeyboardButton("Sell: node", callback_data='sell_node')],
            [InlineKeyboardButton("Buy Slippage: 20%", callback_data='buy_slippage'), InlineKeyboardButton("Sell Slippage: 15%", callback_data='sell_slippage')],
            [InlineKeyboardButton("Back", callback_data='back'), InlineKeyboardButton("🚮Close", callback_data='close')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        last_updated = get_us_time()

        # Settings dashboard content
        message = (
            f"🌸 *Bloom Settings*\n\n"
            f"🟢 : The feature/mode is turned *ON*\n"
            f"🔴 : The feature/mode is turned *OFF*\n\n"
            f"[Learn More!](https://example.com)\n\n"
            f"🕒 Last updated: {last_updated}"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    
    async def show_fee_setting_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Display the fees etting dashboard."""
        self.current_dashboard = "feesetting"
        #Buttons for fee setting dashboard
        keyboard = [
            [InlineKeyboardButton("Buy Fee: 0.001 SOL", callback_data='buy_fee'), InlineKeyboardButton("Sell Fee: 0.001SOL", callback_data='sell_fee')],
            [InlineKeyboardButton("Buy Tip: 0.001 SOL", callback_data='buy_tip'), InlineKeyboardButton("Sell Tip: N/A SOL", callback_data='sell_tip')],
            [InlineKeyboardButton("🔴Auto Tip", callback_data='auto_tip')],
            [InlineKeyboardButton("Back", callback_data='back_to_setting'), InlineKeyboardButton("🚮Close", callback_data='close')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        last_updated = get_us_time()

        # Settings dashboard content
        message = (
            f"🌸 Fee Settings\n\n"
            f"💡Click the button to set your desired fee amount.\n"
            f"Higher fees result in faster transactions.\n\n"
            f"📖 Learn More!\n\n"
            f"🕒 Last updated: {last_updated}"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    
    async def show_buy_presets_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Display the buypresets dashboard."""
        self.current_dashboard = "buypresets"
        #Button for buypresets dashboard
        keyboard = [
            [InlineKeyboardButton("0.5 SOL", callback_data='half_sol'), InlineKeyboardButton("1 SOL", callback_data='one_sol'), InlineKeyboardButton("2 SOL", callback_data='two_sol')],
            [ InlineKeyboardButton("5 SOL", callback_data='five_sol'), InlineKeyboardButton("10 SOL", callback_data='ten_sol')],
            [InlineKeyboardButton("Back", callback_data='back_to_setting'), InlineKeyboardButton("🚮Close", callback_data='close')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        last_updated = get_us_time()

        # Settings dashboard content
        message = (
            f"🌸 Manual Buy Presets\n\n"
            f"Please enter your desired buy amount in SOL.\n"
            f"💡 Click the button to set your desired buy amount.\n\n"
            f"🕒 Last updated: {last_updated}"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    
    async def show_sell_presets_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Display the sellpresets dashboard."""
        self.current_dashboard = "sellpresets"
        #Button for sellpresets dashboard
        keyboard = [
            [InlineKeyboardButton("1 %", callback_data='one_pro'), InlineKeyboardButton("5 %", callback_data='five_pro'), InlineKeyboardButton("10 %", callback_data='ten_pro')],
            [ InlineKeyboardButton("50 %", callback_data='fifty_pro'), InlineKeyboardButton("100 %", callback_data='hundred_pro')],
            [InlineKeyboardButton("Back", callback_data='back_to_setting'), InlineKeyboardButton("🚮Close", callback_data='close')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        last_updated = get_us_time()

        # sell preset dashboard content
        message = (
            f"🌸 Manual Sell Presets\n\n"
            f"Please enter your desired buy amount in SOL.\n"
            f"💡 Click the button to set your desired sell amount.\n\n"
            f"🕒 Last updated: {last_updated}"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    
    async def show_spot_presets_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Display the spot presets dashaboard"""
        self.current_dashboard = "spotpresets"
        #Button for spotpresets dashboard
        button = [
            [InlineKeyboardButton("🆕Create Limit Order", callback_data='create_limit_order')],
            [InlineKeyboardButton("Back", callback_data='back_to_setting'), InlineKeyboardButton("♻️Refresh", callback_data='refresh')],
            [InlineKeyboardButton("🚮Close", callback_data='close')]
        ]
        reply_markup = InlineKeyboardMarkup(button)

        last_updated = get_us_time()

        # spot preset dashboard
        message = (
            f"🌸 Auto Orders\n\n"
            f"🧐 No active limit orders\n\n"
            f"📖 Learn More!\n\n"
            f"🕒 Last updated:  {last_updated}"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    
    async def show_sniper_presets_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Display sniper presets dashboard."""
        self.current_dashboard = "sniperpresets"
        # Button for sniperpresetts dashaboard
        button = [
            [InlineKeyboardButton("🟢 Normal Mode", callback_data='normal_node')],
            [InlineKeyboardButton("Active 🔴", callback_data='sniper_active'), InlineKeyboardButton("💰 Buy amonut : 0 SOL", callback_data='buy_0_sol')],
            [InlineKeyboardButton("💰 Fee : 0 SOL", callback_data='fee_0_sol'), InlineKeyboardButton("🎒 Slippage: 0 %", callback_data='slippage_0')],
            [InlineKeyboardButton("📈 Limit Orders", callback_data='limit_orders')],
            [InlineKeyboardButton("Processsor: Staked Node", callback_data='processor')],
            [InlineKeyboardButton("Back", callback_data='back_to_setting'), InlineKeyboardButton("🚮Close", callback_data='close')]
        ]
        reply_markup = InlineKeyboardMarkup(button)
        
        last_updated = get_us_time()

        # sniperpresetts dashboard
        message = (
            f"🌸 Sniper Presets\n\n"
            f"Please enter your desired sniper settings\n\n"
            f"💡 Click the button to set your desired sniper settings.\n\n"
            f"🟢 Task is active\n\n"
            f"🔴 Task is inactive\n\n"
            f"🕒 Last updated:  {last_updated}"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    
    async def show_degen__mode_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Display the degenmode dashboard."""
        self.current_dashboard = "degemode"
        #Button for dege mode dashboard
        keyboard = [
            [InlineKeyboardButton("🔴 Degen State", callback_data='degen_state')],
            [InlineKeyboardButton("💰 Degen Amount : 0", callback_data='degen_amount_0'), InlineKeyboardButton("💰 Degen Slippage : 0%", callback_data='degen_slippage_0')],
            [InlineKeyboardButton("💰 Min Mcap : N/A USD", callback_data='min_mcap'), InlineKeyboardButton("💰 Max Mcap : N/A USD", callback_data='max_mcap')],
            [InlineKeyboardButton("💰 Min Liq : N/A USD", callback_data='min_liq'), InlineKeyboardButton("💰 Max Liq : N/A USD", callback_data='max_liq')],
            [InlineKeyboardButton("Back", callback_data='back_to_setting'), InlineKeyboardButton("🚮Close", callback_data='close')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        last_updated = get_us_time()

        # sniperpresetts dashboard
        message = (
            f"🌸 Degen Mode Settings\n\n"
            f"⚠️ With Degen Mode ON, the bot buys instantly when the\n\n token address is entered, and won't rebuy after selling, even if\n\nauto-buy is active.\n\n"
            f"🟢: The feature/mode is turned **ON**.\n\n"
            f"🔴: The feature/mode is turned **OFF**.\n\n"
            f"📖 Learn More!"
            f"🕒 Last updated:  {last_updated}"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    
    
    async def show_position_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Display the position settings dashboard."""
        self.current_dashboard = "position"
        # Buttons for position dashboard
        keyboard = [
            [InlineKeyboardButton("Min Value: N/A Sol", callback_data='min_val'), InlineKeyboardButton("♻️Refresh", callback_data='refresh')],
            [InlineKeyboardButton("HomePage", callback_data='homepage'), InlineKeyboardButton("Delete", callback_data='delete')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        last_updated = get_us_time()

        # Position dashboard content
        message = (
            f"🌸 Bloom Positions"
            f"No open positions yet!"
            f"Start your trading journey by pasting a contract address in chat."
            f"🕒 Last updated: {last_updated}"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)

    async def show_sniper_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
        """Display the sniper dashboard."""
        self.current_dashboard = "sniper"

        # Buttons for sniper dashboard
        keyboard = [
            [InlineKeyboardButton("Sniper Wallets:0", callback_data='sniper_wallet'), InlineKeyboardButton("Create Task", callback_data='create_task')],
            [InlineKeyboardButton("Back", callback_data='back'), InlineKeyboardButton("♻️Refresh", callback_data='refresh')],
            [InlineKeyboardButton("🚮Close", callback_data='close')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        last_updated = get_us_time()

        # sniper dashboard content
        message = (
            f"🌸 Bloom Positions\n\n"
            f"🧐 No active sniper tasks!\n\n"
            f"📖 Learn More!\n\n"
            f"🕒 Last updated: {last_updated}\n\n"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)

    async def show_sniper_wallets_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Display the sniper wallets dashboard."""
        self.current_dashboard = "sniperwallets"

        #Buttons for sniperwallets dashboard
        keyboard = [
             [InlineKeyboardButton("🔴W1 - 0 SOL", callback_data='w1_0sol')],
             [InlineKeyboardButton("🔴W2 - 0 SOL", callback_data='s2_0sol')],
             [InlineKeyboardButton("🔴W3 - 0 SOL", callback_data='s3_0sol')],
             [InlineKeyboardButton("Back", callback_data='back'), InlineKeyboardButton("🚮Close", callback_data='close')],
         ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        last_updated = get_us_time()

        # sniper dashboard content
        message = (
            f"🌸 Manage your active sniper wallets\n\n"
            f"Click the button to activate/deactivate a wallet.\n\n"
            f"🟢 Wallet is active\n\n"
            f"🔴 Wallet is inactive\n\n"
            f"🕒 Last updated: {last_updated}\n\n"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)
    
    async def show_trade_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Diaplay the trade dashboard."""
        self.current_dashboard = "trader"

        # Buttons fortrade dashboard
        keyboard = [
            [InlineKeyboardButton("Add new config", callback_data='new_config')],
            [InlineKeyboardButton("Pause All", callback_data='pause_all'), InlineKeyboardButton("Start All", callback_data='start_all')],
            [InlineKeyboardButton("Back", callback_data='back'), InlineKeyboardButton("♻️Refresh", callback_data='refresh')],
            [InlineKeyboardButton("🚮Close", callback_data='close')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        last_updated = get_us_time()

        # trader dashboard content
        message = (
            f"🌸 Bloom Copy Trade\n\n"
            f"💡 Copy the best traders with Bloom!\n\n"
            f"🟢 Copy trade setup is active\n\n"
            f"🔴 Copy trade setup is inactive\n\n"
            f"⏱️ Please wait 10 seconds after each change for it to take effect\n\n"
            f"⚠️ Changing your copy wallet? Remember to remake your tasks to use the new wallet for future transactions.\n\n"
            f"🕒 Last updated: {last_updated}\n\n"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)

    async def show_withdraw_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Diaplay the withdraw dashabord."""
        self.current_dashboard = "withdraw"

        #Button for withdraw dashboard
        keyboard = [
            [InlineKeyboardButton("50%", callback_data='fifty_precent'), InlineKeyboardButton("100 %", callback_data='hundred_percent'), InlineKeyboardButton("X SOL", callback_data='x_sol')],
            [InlineKeyboardButton("Set Address", callback_data='set_address')],
            [InlineKeyboardButton("Back", callback_data='back'), InlineKeyboardButton("♻️Refresh", callback_data='refresh')],
            [InlineKeyboardButton("🚮Close", callback_data='close')] 
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        last_updated = get_us_time()

        # trader dashboard content
        message = (
            f"🌸 Withdraw Solana\n\n"
            f"Balance: 0 SOL\n\n"
            f"Current withdrawal address: \n\n"
            f"🔧 Last address edit: -\n\n"
            f"🕒 Last updated: {last_updated}\n\n"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)

    async def show_wallet_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Display the wallet dashboard."""
        self.current_dashboard = "wallet"

        #Buttons for wallet dashboard
        keyboard = [
            [InlineKeyboardButton("W1 0SOL", callback_data='sol_button1'), InlineKeyboardButton("W2 0SOL", callback_data='sol_button2')],
            [InlineKeyboardButton("W3 0SOL", callback_data='sol_button3')],
            [InlineKeyboardButton("Create Wallet", callback_data='create_wallet'), InlineKeyboardButton("Import Wallet", callback_data='import_wallet')],
            [InlineKeyboardButton("Back", callback_data='back_to_setting'), InlineKeyboardButton("🚮Close", callback_data='close')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        last_updated = get_us_time()

        # Wallet dashboard content
        message = (
            f"🌸 Wallets Settings"
            f"Manage all your wallets with ease."
            f"📖 Learn More!"
            f"🕒 Last updated: {last_updated}"
        )

        await update.callback_query.message.edit_text(message, parse_mode="Markdown", reply_markup=reply_markup)

    async def handle_button_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handles button click events and navigates between dashboards."""
        query = update.callback_query

        if query.data == "afk_mode":
            await self.show_afk_dashboard(update, context)
        elif query.data == "settings":
            await self.show_settings_dashboard(update, context)
        elif query.data == "back":
            await self.show_main_dashboard(update, context)
        elif query.data == "homepage":
            await self.show_main_dashboard(update, context)
        elif query.data == "close":
            await query.message.delete()
        elif query.data == "positions":
            await self.show_position_dashboard(update, context)
        elif query.data == "lp_sniper":
            await self.show_sniper_dashboard(update, context)
        elif query.data == "copy_trade":
            await self.show_trade_dashboard(update, context)
        elif query.data == "wallet":
            await self.show_wallet_dashboard(update, context)
        elif query.data == "back_to_setting":
            await self.show_settings_dashboard(update, context)
        elif query.data == "feesetting":
            await self.show_fee_setting_dashboard(update, context)
        elif query.data == "buy_presets":
            await self.show_buy_presets_dashboard(update, context)
        elif query.data == "sell_presets":
            await self.show_sell_presets_dashboard(update, context)
        elif query.data == "spot_presets":
            await self.show_spot_presets_dashboard(update, context)
        elif query.data == "sniper_presets":
            await self.show_sniper_presets_dashboard(update, context)
        elif query.data == "degen_mode":
            await self.show_degen__mode_dashboard(update, context)
        elif query.data == "sniper_wallet":
            await self.show_sniper_wallets_dashboard(update, context)
        elif query.data == "withdraw":
            await self.show_withdraw_dashboard(update, context)
        elif query.data == "refresh":
            if self.current_dashboard == "main":
                await self.show_main_dashboard(update, context)
            elif self.current_dashboard == "zfk":
                await self.show_afk_dashboard(update, context)
            elif self.current_dashboard == "position":
                await self.show_position_dashboard(update, context)
            elif self.current_dashboard == "setting":
                await self.show_settings_dashboard(update, context)
            elif self.current_dashboard == "wallet":
                await self.show_wallet_dashboard(update, context)
            elif self.current_dashboard == "sniper":
                await self.show_sniper_dashboard(update, context)
            else:
                await self.show_trade_dashboard(update, context)
        else:
            await query.answer()
            await query.edit_message_text(text=f"You clicked: {query.data}")


# Main function to initialize and run the bot
def main() -> None:
    """Run the bot with structured navigation."""
    dashboard_manager = DashboardManager()

    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler('start', dashboard_manager.show_main_dashboard))
    application.add_handler(CallbackQueryHandler(dashboard_manager.handle_button_click))

    # Run the bot
    application.run_polling()


if __name__ == '__main__':
    main()
