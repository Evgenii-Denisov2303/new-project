import random


def random_compliments(lang: str = "ru") -> str:
    return random.choice(COMPLIMENTS.get(lang, COMPLIMENTS["ru"]))


def generate_horoscope(lang: str = "ru") -> str:
    phrases = HOROSCOPE.get(lang, HOROSCOPE["ru"])
    first = random.choice(phrases["first"])
    second = random.choice(phrases["second"])
    third = random.choice(phrases["third"])
    fourth = random.choice(phrases["fourth"])
    return f"{first} {second} {third} {fourth}"


COMPLIMENTS = {
    "ru": (
        "Ты выглядишь лучше всех!",
        "Сегодня будет чудесный день!",
        "Конечно, ты можешь все!",
        "Я никогда не встречал людей добрее тебя!",
        "Очень приятно проводить с вами время!",
        "Ты прекрасно выглядишь!",
        "Я не могу оторвать глаз от твоей улыбки!",
        "У тебя красивые глаза!",
        "С тобой я все забуду!",
        "Я думаю о тебе все время!",
        "У тебя очень чувственные губы!",
        "Я без ума от твоего голоса. Скажи что-нибудь еще!",
        "У вас безупречный вкус!",
        "Счастье – быть с тобой!",
        "С тобой никогда не скучно!",
        "Ты знаешь, как меня рассмешить!",
        "Ты всегда чувствуешь мое настроение!",
        "Ты любишь меня со всеми моими недостатками!",
        "Когда ты держишь меня, все в порядке!",
        "Я могу быть собой, когда ты рядом!",
    ),
    "en": (
        "You look amazing!",
        "Today will be a wonderful day!",
        "You can do anything!",
        "I’ve never met anyone kinder than you!",
        "It’s a joy to spend time with you!",
        "You look great!",
        "I can’t take my eyes off your smile!",
        "You have beautiful eyes!",
        "With you I forget everything!",
        "I think about you all the time!",
        "You have such a lovely voice!",
        "You have impeccable taste!",
        "Happiness is being with you!",
        "You make every day brighter!",
        "You always know how to cheer me up!",
        "You understand my mood so well!",
        "I can be myself when I’m with you!",
        "You make everything feel right!",
        "You are wonderful just as you are!",
        "You are simply the best!",
    ),
    "cs": (
        "Vypadáš úžasně!",
        "Dnes bude krásný den!",
        "Dokážeš úplně všechno!",
        "Nikdy jsem nepotkal někoho milejšího!",
        "Je radost trávit s tebou čas!",
        "Vypadáš skvěle!",
        "Nemůžu odtrhnout oči od tvého úsměvu!",
        "Máš krásné oči!",
        "S tebou zapomínám na všechno!",
        "Myslím na tebe pořád!",
        "Máš nádherný hlas!",
        "Máš bezchybný vkus!",
        "Štěstí je být s tebou!",
        "S tebou se nikdy nenudím!",
        "Umíš mě rozesmát!",
        "Skvěle vycítíš mou náladu!",
        "Můžu být sám sebou, když jsi nablízku!",
        "S tebou je všechno v pořádku!",
        "Jsi skvělý/á takový/á, jaký/á jsi!",
        "Jsi prostě nejlepší!",
    ),
}

HOROSCOPE = {
    "ru": {
        "first": [
            "Сегодня — идеальный день для новых начинаний.",
            "Оптимальный день для того, чтобы решиться на смелый поступок.",
            "Будьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.",
            "Лучшее время для того, чтобы начать новые отношения или разобраться со старыми.",
            "Плодотворный день для того, чтобы разобраться с накопившимися делами.",
        ],
        "second": [
            "Но помните, что даже в этом случае нужно не забывать про",
            "Если поедете за город, заранее подумайте про",
            "Те, кто сегодня нацелен выполнить множество дел, должны помнить про",
            "Если у вас упадок сил, обратите внимание на",
            "Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про",
        ],
        "third": [
            "отношения с друзьями и близкими.",
            "работу и деловые вопросы, которые могут так некстати помешать планам.",
            "себя и своё здоровье, иначе к вечеру возможен полный раздрай.",
            "бытовые вопросы — особенно те, которые вы не доделали вчера.",
            "отдых, чтобы не превратить себя в загнанную лошадь в конце месяца.",
        ],
        "fourth": [
            "Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.",
            "Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.",
            "Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела до конца.",
            "Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.",
            "Если встретите незнакомца на пути — проявите участие, и тогда эта встреча посулит вам приятные хлопоты.",
        ],
    },
    "en": {
        "first": [
            "Today is a great day for new beginnings.",
            "A perfect day to take a bold step forward.",
            "Be careful — the stars may affect your finances today.",
            "A good time to start new relationships or sort out old ones.",
            "A productive day to deal with pending tasks.",
        ],
        "second": [
            "But remember to pay attention to",
            "If you travel out of town, think in advance about",
            "Those aiming to do many things today should remember",
            "If you feel low on energy, focus on",
            "Remember that thoughts are powerful, so keep in mind",
        ],
        "third": [
            "your relationships with friends and family.",
            "work and business matters that could disrupt your plans.",
            "yourself and your health, otherwise the evening may be chaotic.",
            "household tasks — especially the ones you left unfinished yesterday.",
            "rest, so you don’t burn out by the end of the month.",
        ],
        "fourth": [
            "Ignore the doubters today.",
            "Success favors the persistent — strengthen your resolve.",
            "Even if Mercury is retrograde, finish what you started.",
            "Don’t be afraid of lonely meetings — they can matter a lot today.",
            "If you meet a stranger, show kindness, and it will bring pleasant surprises.",
        ],
    },
    "cs": {
        "first": [
            "Dnes je skvělý den pro nové začátky.",
            "Ideální čas udělat odvážný krok.",
            "Buď opatrný/á — hvězdy mohou ovlivnit finance.",
            "Dobrá doba začít nové vztahy nebo vyřešit staré.",
            "Plodný den pro vyřízení odložených věcí.",
        ],
        "second": [
            "Ale pamatuj, že je důležité myslet na",
            "Pokud pojedeš mimo město, mysli dopředu na",
            "Ti, kteří chtějí stihnout hodně věcí, by neměli zapomenout na",
            "Pokud máš málo energie, zaměř se na",
            "Pamatuj, že myšlenky jsou silné, proto mysli na",
        ],
        "third": [
            "vztahy s přáteli a rodinou.",
            "práci a obchodní záležitosti, které mohou narušit plány.",
            "sebe a své zdraví, jinak může být večer chaotický.",
            "domácí povinnosti — hlavně ty, co zůstaly včera.",
            "odpočinek, aby ses na konci měsíce nevyčerpal/a.",
        ],
        "fourth": [
            "Nevěř pomluvám, dnes jim nenaslouchej.",
            "Úspěch přeje vytrvalým — posiluj svou vůli.",
            "I když je Merkur retrográdní, dokonči rozdělané věci.",
            "Neboj se osamělých setkání — dnes mohou hodně znamenat.",
            "Potkáš-li cizince, buď laskavý/á a přinese to příjemné překvapení.",
        ],
    },
}
