# -*- coding:utf-8 -*-

from project_DY.animation import Animation

Confs = {
    "The Eye of Horus": {    # title
        "title": "The Eye of Horus",
        "w": 540,
        "h": 960,
        "fps":30,
        "img": "eye.webp",
        "desc": "荷鲁斯之眼",
        # "font": "",
        "font_size": 32,
    },
    "Valknut": {
        "title": "Valknut",
        "dir": "Valknut",
        "w": 540,
        "h": 960,
        "fps":30,
        "img": "Valknut.png",
        # "font": "",
        "font_size": 36,
        "desc": "对于北欧神话来说,Valknut是最具有代表性的古老神秘符号之一.从视觉上看，它由三个互相连锁的三角形组成。考古学上，它出现在几块可追溯到维京时代、矗立在瑞典的哥得兰岛上的象形石和图案纪念石上，也出现在挪威奥塞伯格船葬的墓葬物品上。它的名字在任何时期的资料中都没有提到; 而valknut 是一个现代挪威复合词，意思是“战死沙场的人的结”，是在维京时代之后很久的挪威人引进的.其真正的文化含义暂时未知,但有如下的说法."
                "其一,由于这个符号出现在奥丁的画像石和奥塞伯格船葬的葬礼礼物上，与奥丁息息相关,而奥丁作为北欧神话中众神之父\战争之神,创建了英灵神殿以接纳英勇无畏死去的亡灵,所以出现在墓葬品上的这个符号,自然成为了奥丁的标志亦或者说英灵神殿的标志,人们猜测其与死亡相关."
                "其二,部分学者称其为赫伦尼尔之心(Hrungnir's heart, 北欧神话中的巨人，最后被雷神之锤杀死)。其说法是源于13世纪埃达散文集《 Skáldskaparmál 》的第17章对其心脏进行了如下描述: “ Hrungnir 有一颗著名的心脏。它由坚硬的石头制成，有三个尖角，就像雕刻的符号。",
    },
    "Mjolnir": {
        "title": "Mjolnir",
        "dir": "Mjolnir",
        "w": 540,
        "h": 960,
        "fps":30,
        "img": "Mjolnir.jpg",
        # "font": "",
        "font_size": 32,
        "desc": "雷神之锤，象征着保护、力量、神圣.雷神托尔的武器，既被用作毁灭，也被用作祝福的神圣工具。这把锤子有许多文献记载，如13世纪编纂的埃迪克散文诗集《诗歌埃达》《散文埃达》,人们通常把雷神之锤当作维京时代的挂件佩戴。",
        "summary": "雷神之锤，象征着保护、力量、神圣,可用作护身符。"
    },
    "Troll Cross": {
        "title": "Troll Cross",
        "dir": "Troll Cross",
        "w": 540,
        "h": 960,
        "fps":30,
        "img": "Troll Cross.png",
        # "font": "",
        "font_size": 32,
        "desc": "巨魔十字架,在瑞典和挪威，巨魔十字架是一块弯曲形状的金属，被戴在身上作为护身符来抵御邪恶的魔法，据说起源于中世纪的瑞典。它代表了北欧保护的象征; 对北欧人而言，这个象征会减少他们陷入危险的机会。",
        "summary": "巨魔十字架，用来抵御巨魔和精灵以及邪恶魔法,可用作护身符。"
    },
    "Helm of Awe": {
        "title": "Helm of Awe",
        "dir": "Helm of Awe",
        "w": 540,
        "h": 960,
        "fps":20,
        "img": "helm of awe.png",
        # "font": "",
        "font_size": 32,
        "desc": "敬畏之舵。古北欧非常流行的一个魔法符文,象征着保护和力量,所激发的保护不仅仅是身体上的,同时也在精神层面，它可以在敌人心中制造恐惧和压制自己内心恐惧。",
        "summary": "敬畏之舵。古北欧非常流行的一个魔法符文,象征着保护和力量,所激发的保护不仅仅是身体上的,同时也在精神层面，它可以在敌人心中制造恐惧和压制自己内心恐惧"
    },
    "Vegvisir": {
        "title": "Vegvisir",
        "dir": "Vegvisir",
        "w": 540,
        "h": 960,
        "fps":20,
        "img": "Vegvisir.png",
        # "font": "",
        "font_size": 32,
        "desc": "罗盘符文,一个来自近现代冰岛魔法手稿的符号,被视为幸运、保护和祝福的护身符。这个符号可以让人在暴风雨或恶劣天气中找到正确的道路，即使前路未知。同时作为一个精神指南针，它将引导你的内心做出正确的选择,哪怕已经失去信仰.",
        "summary": ""
    },
    "swastika": {
        "title": "swastika",
        "dir": "swastika",
        "w": 540,
        "h": 960,
        "fps":20,
        "img": "swastika.jpg",
        # "font": "",
        "font_size": 32,
        "desc": "日轮,在诸多宗教中文化中都有出现的一个古老符号,如印度教、佛教等,本是精神和神性的象征.直至二战纳粹将其占领,因其所作所为,如今在众多国家依然被禁止.",
        "summary": ""
    },
    "Svefnthorn": {
        "title": "Svefnthorn",
        "dir": "Svefnthorn",
        "w": 540,
        "h": 960,
        "fps":20,
        "img": "Svefnthorn.jpg",
        # "font": "",
        "font_size": 32,
        "desc": "使对手陷入长时间不会醒来的沉睡之中",
        "summary": "使对手陷入长时间不会醒来的沉睡之中"
    },
    "Web of Wyrd": {
        "title": "Web of Wyrd",
        "dir": "Web of Wyrd",
        "w": 540,
        "h": 960,
        "fps":20,
        "img": "Web of Wyrd.jpg",
        # "font": "",
        "font_size": 32,
        "desc": "命运之网,3组平行共9条直线交织成的符号,网格代表着过去\现在\未来相互交融,彼此影响,蕴含着生命命运的真谛",
        "summary": ""
    },
    "Yggdrasil": {
        "title": "Yggdrasil",
        "dir": "Yggdrasil",
        "w": 540,
        "h": 960,
        "fps":20,
        "img": "Yggdrasil.jpg",
        # "font": "",
        "font_size": 32,
        "desc": "世界之树,生长在挪威宇宙的中心,连接并孕育着9个世界,宇宙万物相互联系的象征图形",
        "summary": ""
    },
}

class Runner():
    def progress(self, title):
        conf = Confs.get(title, )
        if not conf:
            print("找不到配置", title)
            return
        Animation(f"./imgs/{conf['img']}", conf['title'], w=conf['w'], h=conf['h'], fps=conf['fps'],
                  title_font_size=conf['font_size'], dir_=conf.get("dir", '')).run()
        print("描述:",)
        print(conf['desc'])

if __name__ == '__main__':
    # Runner().progress('The Eye of Horus')
    # Runner().progress('Valknut')
    # Runner().progress('Mjolnir')
    # Runner().progress('Troll Cross')
    # Runner().progress('Helm of Awe')
    # Runner().progress('Vegvisir')
    # Runner().progress('swastika')
    # Runner().progress('Svefnthorn')
    # Runner().progress('Web of Wyrd')
    Runner().progress('Yggdrasil')