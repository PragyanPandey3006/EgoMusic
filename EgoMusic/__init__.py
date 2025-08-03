from EgoMusic.core.bot import Ego
from EgoMusic.core.dir import dirr
from EgoMusic.core.git import git
from EgoMusic.core.userbot import Userbot
from EgoMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Ego()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
