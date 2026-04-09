"""
便秘一言金句库

包含各种逆天、猎奇、重口味的厕所文学金句
来源：贴吧、小红书、抖音、知乎等全网平台
"""

import random
from typing import Any, Optional

from astrbot.api import logger

CONSTIPATION_QUOTES = [
    # ===== 经典网络神梗 =====
    "屎：开门！肛：谁？屎：屁。",
    "成年人的崩溃从发现厕所没纸开始，重生从摸到口袋里的餐巾纸开始。",
    "人生就像冲马桶，有时候需要多按几次才能解决问题。",
    "带薪拉屎指南：如厕时长≈刷三个短视频，请自觉控制流量套餐。",
    "智能马桶检测到用户压力值超标，自动播放：'朋友，你需要的不是如厕，是辞职'",
    "忘带手机进厕所，结果发现墙上贴着前任写的：'到此一游，想你'",
    "当你在厕所隔间听到同事声音时：该打招呼还是屏住呼吸？",
    "醉汉抱着马桶喊：'这出租车座椅怎么是凉的？'",
    "孩子问为什么厕所叫'洗手间'，我回答：'因为有些人进去真的只洗手'",
    "建议在写字楼厕所安装刷卡系统：VIP会员可享受加热坐垫和优先冲水权",
    "自动感应冲水马桶在你刚蹲下时就冲水，仿佛在说：'放弃吧，你没戏了'",
    "厕所标语：'冲水键不是俄罗斯轮盘赌，按两次算你输！'",
    
    # ===== 2025年毒舌歇后语 =====
    "癞蛤蟆追青蛙——长得丑玩得花",
    "屎壳郎戴面具——臭不要脸",
    "骨灰盒里放响屁——正宗阴间操作",
    "厕所里跳高——过粪（分）了",
    "老母猪戴胸罩——一套又一套",
    "秃子打伞——无法（发）无天",
    "王八退房——憋（鳖）不住了",
    "被窝里放屁——能文（闻）能武（捂）",
    "肚脐眼放屁——你咋响（想）的",
    "电线杆上绑鸡毛——好大的掸（胆）子",
    "小蜜蜂摸高压线——直接麻成蜂干儿",
    "QQ农场响了——你菜死了",
    "共享单车去酒吧——该省省该花花",
    "熊猫开直播——笋（损）出新高度",
    "口袋里装钉子——个个想出头",
    "挨着火炉吃辣椒——里外发烧",
    "乌龟办走读——憋不住笑（校）了",
    "八二年的龙井——老绿茶了",
    "玉皇大帝放屁——神气",
    "纱布擦屁股——给我漏了一手",
    "坟头拉二胡——鬼扯",
    "上坟烧报纸——糊弄鬼呢",
    "老母猪卡栅栏——进退两男（难）",
    "老太太喝稀饭——无耻（齿）下流",
    "光屁股坐板凳——有板有眼",
    
    # ===== 小红书/抖音厕所文学 =====
    "每个人拉屎的时候都是一只裱花袋",
    "马桶：'这落座声…是自由落体实验吧？'",
    "挤牙膏般便秘 → 痛苦面具😫",
    "一泻千里的瞬间——'这冲水声…是《命运交响曲》的高潮乐章！🎻'",
    "回头看一眼：'今日份作品…是抽象派还是写实派？'🖼️",
    "会议中放无声屁 → 化身毒气刺客🗡️（同事：'突然有种…生命流逝的感觉'）",
    "被窝里自产自销 → 沼气池爱情故事💑",
    "他们说人生要有理想——我的理想是每天准时打卡⏰（马桶：'你倒是冲啊！！'）",
    "不是闹钟叫醒我，是结肠的紧急集合哨🚨——'全体注意！五分钟后全军出击！'",
    "50米跨栏选手看了都沉默🤸",
    
    # ===== 优雅上厕所说法 =====
    "吾去去便回，各位勿念",
    "朕去去便回",
    "我的臀部想吐，先失陪一下",
    "大肠的挽留，终究抵不过纸的温柔",
    "马桶饿了，我去给它送饭",
    "我要去一趟五谷轮回的地方",
    "我去排解下忧愁",
    "我现在有个机会可以瘦一斤，失陪下",
    "我去做一个褐黄色的小蛋糕",
    "月亮姐姐邀我共舞，我去应个邀",
    "大肠使者召唤，吾得去觐见",
    "吾要去和马桶共度美好时光",
    "五谷轮回之地，邀我共赴盛宴",
    
    # ===== 贴吧神回复 =====
    "人生自古谁无死，拉屎不用纸的是勇士",
    "便秘不是病，拉不出来真要命",
    "有一种痛，叫明明有感觉却拉不出来",
    "世界上最遥远的距离，是我在马桶上，纸在门外",
    "拉屎五分钟，蹲坑半小时——现代人的生活写照",
    "不要问我为什么这么久，我在和肠道做斗争",
    "肠道不通，万事皆空",
    "一鼓作气，再而衰，三而竭——便秘者的悲歌",
    "今天不拉屎，明天徒伤悲",
    "早拉早轻松，晚拉一场空",
    "我在所里办点事，各位慢聊",
    "忧愁缠绕，吾去寻求解脱",
    "天赐良机，减去一斤凡尘",
    
    # ===== 职场如厕潜规则 =====
    "为什么我能成为时间管理大师？因为我连蹲坑都在刷剧办公！",
    "公司新装的风干机风力太强，每次洗手都感觉自己要起飞",
    "外国友人对中国公厕的蹲坑发出灵魂拷问：'这是要我做深蹲训练吗？'",
    "公厕标语：'本座已渡劫成功，投币可续命'",
    "每天到公司的第一件事情：就是看看领导工位上有没有人",
    "这一届的小孩的确可怕，上一届的小孩还只是在厕所里跟我说老师好，这一届的小孩是看到我进厕所了就朝厕所大喊：'我老师来了，你们都夹断把坑位让给我老师！'",
    
    # ===== 沙雕文案 =====
    "我努力3分钟没看到回报我就不想努力了",
    "我说我在忙，你知道我在忙就行了，就别问我在忙什么了，我还得编",
    "终于找到了让人变自信的方法：遇到问题时，只要说'我自有打算'，就能显得很自信，一切尽在掌握中，其实我是打算啥也不干",
    "之前不理解为什么李白会写这么多诗词，我自己出去玩了一趟，一天发了二十条朋友圈",
    "说多少遍了我不是小丑，只是最近天气降温了，鼻子红红的很正常",
    
    # ===== 英文梗翻译 =====
    "Poop jokes aren't my favorite... but they're a solid number two",
    "为什么马桶从不去派对？因为它们总是被冲走(Flush)",
    "马桶纸最喜欢的游戏？Hide and leak（捉迷藏+漏）",
    "为什么马桶纸滚下山？为了到达底部(To get to the bottom)",
    "如何给马桶加油？给它一个皇家冲洗(Royal flush)",
    " constipation（便秘）的电影为什么没上映？因为它一直没出来(never came out)",
    
    # ===== 恐怖/悬疑故事 =====
    "在公厕发现没带纸，急中生智敲隔壁隔板：'兄弟借点纸？'沉默五秒后传来女声：'大哥，是你进错了还是我进错了？'",
    "忘带手机进厕所，结果发现墙上贴着前任写的：'到此一游，想你'",
    "自动感应冲水马桶在你刚蹲下时就冲水，仿佛在说：'放弃吧，你没戏了'",
    
    # ===== 九转大肠梗 =====
    "九转大肠——保留本味，原汁原味",
    "甲方说'就要这感觉'，打工人默默甩链接，意思是我没改，原汁原味",
    "评委咬到原味肥油，脸皱成抹布",
    
    # ===== 物理/化学梗 =====
    "公司新装的风干机风力太强，每次洗手都感觉自己要起飞",
    "如果被窝是沼气池，那我就是产气专家",
    "我的肠道正在进行一场自由落体实验",
    
    # ===== 新增猎奇内容 =====
    "蹲坑刷到'蹲下请瞄准'，差点笑到腿麻——原来全国女厕所正在偷偷换新标语",
    "男厕标语：'向前一小步文明一大步'，女厕：'蹲下请瞄准'",
    "厕所连环炸坑，谁没试过？",
    "七天不到，同款句式攻占男厕、地铁、公司厕所门，像溅出来的水花",
    "碎片越滚越快，抖音、小红书负责点火，微信表情包负责收尸",
    "速生速死，像泡面，三分钟香，五分钟腻",
    "下次蹲坑再刷到新标语，别惊讶，笑完就忘，才是正常节奏",
    "79%的人刷到这类内容会笑，笑完61%会转发——图个啥？释放压力，换点社交筹码",
    "知道'九转大肠'等于拿到入场券，不懂梗连群聊都插不上话",
    "平均每人每天撞见二十多次，停留却不到半分钟",
    
    # ===== 更多逆天 =====
    "我有一室友特胆小，晚上一人在厕所大号，突然'啊'的一声尖叫打破了夜的寂静，那声音，仿佛见了鬼似的",
    "推开门一看，好家伙，这货正坐在马桶上，脸色煞白，眼睛瞪得像铜铃。我忙问咋回事，他结结巴巴地说：'刚……刚才好像有只老鼠从我脚边跑过。'我往地上一瞧，哪有什么老鼠呀",
    "从那以后，他每次晚上去厕所，都得先在门口大喊几声，给自己壮壮胆",
    "有次我故意在厕所里弄出点动静，他在外面听到后，那反应绝了，直接抱着枕头冲进了宿舍，边跑还边喊：'救命啊，有鬼啊！'",
    "他在厕所正进行到'关键时刻'，突然外面刮起一阵大风，把门吹得'哐当'一声响。他'嗷'的一嗓子就从马桶上蹦了起来，提都没提裤子，就准备往外冲",
    
    # ===== 扬州黄瓜事件改编 =====
    "听说有人用黄瓜刺激排便，结果黄瓜直接滑进体内取不出来了",
    "还有人把活黄鳝塞进肛门，结果黄鳝直接钻进肚子里",
    "小时候吃多了野李子，便秘难受，妈妈直接把肥皂削成圆条",
    "便秘时，我们应该多从调整生活习惯入手，多吃蔬菜水果，适度运动，养成良好的作息",
    "千万别再盲目尝试这些奇葩偏方，不然不仅解决不了问题，还可能让自己遭更大的罪",
    
    # ===== 巨型大便梗 =====
    "上厕所的时候拉出了巨型粑粑，结果在冲水的时候遇到难题：无法冲下去",
    "最后凭借着聪明才智和丰富经验巧妙化解",
    "老板：我这是洗车坊，不是澡堂",
    "新买的大姜pocket3真不赖，能拍照能做菜",
    "关于冲厕所的大型交流论坛，网友们对此颇有研究",
    
    # ===== 终极哲学 =====
    "人生三急，在这种人生的关键时刻最怕打开厕所门，发现上一位朋友留下的惊喜",
    "感受下今日份的沙雕鉴赏《关于冲厕所的大型交流论坛》",
    "一起来瞅瞅，感受下今日份的沙雕鉴赏",
    "俗话说人有三急，在这种人生的关键时刻最怕打开厕所门，发现上一位朋友留下的惊喜",
    
    # ===== B站/知乎神回复 =====
    "公厕，这个既公共又私密的空间容纳着人类蹲坑时的无聊与隐匿的宣泄",
    "弹幕般的女厕墙似乎有种魔力，能激发出路人挡不住的创作激情",
    "厕所文学拯救文荒",
    "人有三急很正常，结果去把亲戚家的厕所给拉堵了",
    "操纵便量法竟然应用在这里了，他真是个天才吧",
    "看到这段文字，我已经窒息了，好社死的事，这不得逃离地球？",
    "狠人！不行，我洁癖犯了~",
    "佩服我自己，还去想象了一下爆那个画面，太刺激了",
    "吉日没选好这是！",
    "求你大姨心理活动~",
    "没关系啊，悄悄出去反正人多……",
    "确实是相当有实力，孩子的一次生气换来一辈子的内向！",
    "哈哈哈，我是不想笑，不过真的很好笑哈哈哈哈",
    "对呀，扔哪了？换成我的话，我会跟我妈说拉堵了让她来给我收拾烂摊子",
    "哈哈哈，告示看似是给所有人看的，实际是你专享的",
    "服了，我的实力也是我家公认的！",
    
    # ===== WiFi信号梗 =====
    "蹲厕所刷剧正到高潮，WiFi信号突然跳水成一格。我举着手机在马桶上扭成麻花，一会儿踮脚一会儿蹲马步，活像在跳奇怪的健身操",
    "老婆在门外喊：'你再不出来，我以为你在里面练瑜伽呢！'结果手机'啪嗒'掉地上，信号反倒满格了",
    "怀疑我家路由器是个'势利眼'，客厅追剧秒加载，一进厕所就卡成PPT",
    "昨天蹲厕所刷短视频，画面里的人张嘴三分钟才出声，我对着手机喊：'你倒是说话啊！'旁边猫蹲在门口看我，仿佛在说：'人类为了个破信号，真可怜'",
    "拿着手机在厕所跟WiFi信号'谈判'：'你给我满格，我明天就给路由器换个新位置'",
    "老婆推门进来：'你跟谁说话呢？手里还攥着卫生纸挥舞，要起义啊？'",
    "为了蹭到厕所那微弱的WiFi，我蹲了足足半小时，腿麻得站不起来",
    "好不容易扶着墙挪出去，老公问：'你便秘了？'我举着手机哭丧脸：'不是，是WiFi信号绑着我不让走，它赢了，我腿麻了'",
    "公司厕所的WiFi比老板的脸还难捉摸",
    "同事小张昨天在厕所抢红包，举着手机贴在天花板上，结果红包没抢到，头撞了个包",
    "今天他带了个梯子进去，领导路过问：'你这是要在厕所修灯？'小张苦着脸：'抢红包专用设备'",
    "我家WiFi好像有'地域歧视'，主卧、客厅、厨房信号都好好的，唯独厕所像被下了诅咒",
    "昨天朋友来家里，我让他在厕所试试信号，他进去两分钟就出来：'你家厕所是不是得罪WiFi了？'",
    "蹲厕所时WiFi信号差，我把藏在抽屉里的饼干拿出来，对着路由器方向晃了晃：'给你闻闻香味，换个满格信号呗'",
    "结果信号没变好，倒把隔壁房间的狗引来了，扒着厕所门'汪汪'叫，吓得我手里的饼干都掉了",
    "为了找到厕所里WiFi信号最好的位置，我像个侦察兵一样，拿着手机在厕所里来回踱步，标记了好几个点",
    "老公进来看到地上的粉笔印，疑惑地问：'你这是在厕所画藏宝图呢？'我严肃地说：'比藏宝图重要，这是信号分布图'",
    "每天早上厕所WiFi信号还行，一到晚上就罢工",
    "昨晚我蹲厕所刷剧，信号卡得人物都成了马赛克，我对着手机喊：'你是白天上班太累了，晚上要休息吗？'结果手机自动关机了，合着它是真累了",
    "蹲厕所时WiFi信号时好时坏，我一会儿站着一会儿坐着，跟它展开拉锯战",
    "好不容易信号稳定了，刚想点开视频，儿子在门外喊：'妈妈，路由器被我拔了，我想看看它亮不亮！'我瞬间石化，这熊孩子简直是信号杀手",
    "闺蜜来我家，吐槽我家厕所WiFi信号差，我说：'它可能是想让你专心上厕所，别玩手机'",
    "闺蜜不信，非要举着手机在厕所里转圈，结果不小心撞到了马桶，捂着额头说：'行，它赢了，我给它磕一个还不行吗？'",
    "发现一个规律，只要我家厕所WiFi信号突然变好，准是要下雨",
    "昨天信号罕见满格，我赶紧提醒老公收衣服，老公半信半疑，结果半小时后果然下起了大雨。现在我家厕所WiFi成了免费天气预报员",
    "蹲厕所时WiFi信号差，我无聊就唱歌给它听：'你是我天边最美的云彩，让我用心把你留下来！'唱了三遍，信号居然真的多了一格",
    "我正高兴，楼下邻居敲天花板：'楼上的，唱歌能不能换个地方，厕所回音太大了！'",
    "晚上起夜，路过路由器时，好像听到它在小声嘀咕：'厕所那个地方，信号懒得去，又暗又臭'",
    "我气不过，把路由器转了个方向，对着厕所。结果第二天厕所信号还是差，合着它还挺有脾气，说不去就不去",
    "昨天蹲厕所刷快递物流，WiFi信号卡得一动不动。我急得直跺脚，刚想站起来，信号突然好了，物流显示'快递正在派送中'",
    "我怀疑WiFi是故意的，就等着看我着急的样子，太坏了",
    "在我家厕所，想用好WiFi得遵守'生存法则'：不能蹲太久，不能离门太远，不能大声说话",
    "上次我蹲太久，信号直接消失，吓得我赶紧提裤子出来，结果一到客厅，信号又满格了，这WiFi简直是个傲娇的小家伙",
    
    # ===== 便秘治疗梗 =====
    "便秘患者们倾诉着难言之隐，还根据自己的治疗和调理经验，整理发布了众多便秘'自救秘方'",
    "在诸如'便秘星人看过来，这个方法超有效''告别便秘，我终于可以畅快呼吸'的分享中，网友们为便秘找到了'解救神器'",
    "膳食纤维补充、中医穴位按摩、果蔬汁通便法、定时排便训练、益生菌摄入、运动改善、特定蹲便姿势……这些方法真的能攻克便秘难题吗？",
    "有网友戏称便秘为'现代青年的隐秘烦恼'",
    "今天脚都蹲麻了，甚至要哭出来了，依然没有便意",
    "每天都在斗争，啥时候是个头啊",
    "我今天也没有排便，好苦恼",
    "一般一周排便少于两次，即3天以上没有排便，且排便困难伴有身体不适，这种情况可判定为便秘",
    "如果每天都能排便，但排便过程很困难、费力，时间较长，比如超过10分钟且身体不舒服，也属于便秘范畴",
    "一些年轻人偏爱辛辣、油腻食物，且喝水少、蔬菜水果摄入少，这会加重肠道负担，使肠道蠕动减缓，引起便秘",
    "还有些人因工作忙或其他原因，在有便意时选择抑制排便，久而久之，粪便会逆蠕动，回到直肠上方至乙状结肠，形成坏习惯",
    "熬夜在年轻人中已成为一种生活常态，而这一习惯对肠道健康极为不利",
    "熬夜会使水分摄入减少，同时身体活动量也降低，导致肠道缺乏水分滋润和运动刺激，从而容易引发便秘",
    "补充膳食纤维对肠道蠕动有益。摄入足够量的膳食纤维，可以有效缓解便秘",
    "按摩神阙穴，即围绕腹部肚脐周围，适度用力，精神集中，经常做顺时针、逆时针各几十下的按摩，可以刺激肠道主动蠕动",
    "训练自己养成定时排便的习惯也是一种有效的方法",
    "人体排便有一种反射，如果能养成定时定点的规律，如早晨起床就去厕所，无论有无便意都蹲一下，形成生物钟，有助于防止便秘",
    "每次如厕时间不宜过长，最好不超过5分钟，否则可能引起其他肛肠和肛周疾病",
    "快走是促进肠道蠕动的较好方式。每天坚持半小时的快走，可使交感神经放松，副交感神经发挥作用，从而促进肠蠕动",
    "蹲坑时肛门直肠角度有助于大便排出，能把直肠角度拉直，相比坐便更有利于排便",
    "在坐便时看书、玩手机等行为，会转移注意力，不利于排便",
    "长期便秘会导致人体代谢内分泌失衡，可能出现脸上长痘、皮肤粗糙等情况，还会引起情绪问题，如烦躁、焦虑等",
    "长期便秘可能增加肠道疾病风险，如痔疮、肛裂等",
    "对于中老年人，用力排便还可能引发心脑血管意外",
    "要预防便秘，首先要养成良好的生活习惯，有便意时及时排便，不要久忍",
    "饮食上要多吃蔬菜水果，多喝水；适当运动，避免熬夜",
    
    # ===== 奇怪姿势梗 =====
    "坐在马桶上，双腿微微打开，两个手肘架在膝盖上，双手交叉用力紧握，上半身用力下压，集中精力，想象肠子推着粑粑往下走的感觉",
    "实在不行，还可以搭配上脚底的动作，抬起后脚跟并不断向下踩，据说保持2~3分钟就可以将肚子排空",
    "在正常站立或坐姿时，直肠和肛门之间形成一个'肛直角'，大约是80°~90°，能有效阻止了粪便排出",
    "当我们蹲着的时候，耻骨直肠肌松弛，导致肛直角变大，肛门与直肠的连接就更通畅，方便粪便排出",
    "蹲便时，大腿紧贴腹部，导致腹压高，也就更容易排便",
    "如果家里用的是马桶，可以在卫生间放一个小凳子，用于排便时放脚",
    
    # ===== 英文梗 =====
    "Good news: I'm not lactose intolerant. Bad news: gestures vaguely at stomach",
    "My insides right now are like a game of Tetris…and I can't for the life of me figure out how to make this brick fit!",
    "My gastrointestinal tract is about as active as a sloth on vacation",
    "Why don't they have plumbing in Hogwarts? Because Harry Potter always clogs the 'Chamber of Secrets'",
    "What's the definition of 'split second' decision making? A constipated person with diarrhea and a trampoline",
    "Did you hear about the constipated mathematician? He worked it out with a pencil",
    "My friend said his new job is really 'moving.' Turns out, he's a laxative salesman",
    "I just wrote a book about constipation. I haven't finished it yet though, it's still in the drafts",
    "What do you call a superhero who fights constipation? Captain Fiber!",
    "You know you've eaten too much fiber when…you have to break wind in Morse code",
    "What do you call a bear with digestive problems? A consti-poo-lated bear!",
    "Why is it so hard for ghosts to use the toilet? They're always getting lost in the ethereal plane… and the plumbing",
    "I used to be addicted to laxatives…but I'm finally ready to move on… in a healthy and natural way",
    "I'm feeling really backed up with work. I guess you could say I've got a serious case of job constipation",
    "Heard about the constipated mathematician? He worked it out with a pencil",
    "I told my therapist about my constant fear of portable toilets. He said, 'You need to come out of your comfort zone.' I replied, 'That's the problem, doc.'",
    "They say constipation is hereditary. That's crap, if you ask me",
    "What do you call a fiber supplement that's always in a rush? Consti-pation!",
    "I tried to write a song about constipation. Turns out, it was a real struggle to get out",
    "My doctor told me to avoid constipating foods. So, I gave him a blank stare",
    "I saw a sign that said 'Beware: Constipated Dogs.' Seemed like a lot of pressure",
    "My stomach's been feeling a bit 'off-key' lately. Guess you could say it's suffering from a bad case of… consti-nation",
    "Why don't they have plumbing in the jungle? Because it's all water closets!",
    "You know what they say: 'If you don't go after what you want, you'll never get it.' Unless, of course, it's constipation",
    "What's the opposite of a 'lax' security guard? One who takes their job very… regularly",
    "I used to be a plumber for the Queen. I was the master of the royal flush!",
    "People always ask, 'What's brown and sounds like a bell?' I say, 'Dung!'",
    "My friend told me he was writing a book on constipation. He said it was really coming along slowly",
    "Constipation is a real pain in the… well, you know",
    "I tried to have a philosophical debate about the nature of constipation, but it went nowhere fast",
    "My doctor gave me good news and bad news about my constipation. The good news is, it's not cancerous. The bad news is, it's immortal",
    "My resolution this year was to be less backed up on my work…and then I got constipation. Irony is cruel",
    "Constipation: Proof that you can be full of it and still feel empty inside",
    "Tried to pay for my coffee with prunes. Apparently, they don't accept 'fiber currency.'",
    "Just saw a sign that said, 'Restroom for Customers Only.' Guess I'll have to buy this constipation from someone else",
    "Heard scientists are developing a teleportation device for people with constipation. They're just having trouble getting the kinks worked out",
    "My gastrointestinal tract is like a motivational speaker right now… all talk, no action",
    "Constipation is like writer's block, but instead of a story, it's…well, you get the idea",
    "Never trust a fart when you're constipated. It's probably a bluff",
    "Q: What do you call a superhero who battles constipation? A: Fiber Man!",
    "Q: Why did the constipated mathematician struggle with fractions? A: He couldn't divide and conquer!",
    "Q: What's the opposite of a casual acquaintance? A: A constipated acquaintance – they take a long time to pass!",
    "Q: What do you call a motivational speaker who specializes in digestive health? A: A stool-inspiring figure!",
    "Q: What does a constipated ghost say? A: 'Boo hoo… boo hoo… ooooh, that's better.'",
    "Q: Why don't they have plumbing in Transylvania? A: Because Dracula keeps 'sta",
    
    # ===== 女厕马桶争议 =====
    "我真的不知道上哪去提意见，才能把女厕所的那个马桶给取消！我真的很想让女厕的马桶没有！",
    "你别以为整马桶看着像挺文明的，看着像挺干净，但实际上没有一个人不是拿脚踩的，不是拿尿呲的，不是半蹲的，不能那么干净",
    "蹲坑还是马桶？网友吵翻",
    "有人还对取消马桶这个提议进行了补充完善，比如马桶配备一次性马桶垫等清洁设备，不完全取消马桶但要增加蹲便位",
    "蹲便位不要设计自动冲水功能等等",
    "一刀切的取消女厕马桶不能解决问题，最核心的点还是女厕卫生条件不高",
    "应该做的是通过提供一次性马桶垫等卫生用品来提高卫生条件，而不是取消马桶",
    "一些所谓出于卫生考虑采取的特殊如厕方式，反而是加剧大众对女厕卫生担忧的原因",
    "担心马桶太脏，选择悬空在马桶上如厕，反而容易弄脏马桶甚至地面；蹲在马桶上如厕，更是绝对会弄脏马桶，甚至直接把马桶弄塌",
    "因为上厕所而传染上性病的几率可以说是微乎其微",
    "性病全称是性传播疾病，一般是发生性行为后传染的，感染条件为生殖器官或肛门处有足够多的病菌",
    "性病病原体离开人体后，自体存活时间不长",
    "性病毒要通过马桶传播，要满足这几个条件，首先刚好前一个用过马桶的人有性病而且留下了大量新鲜的精液或阴道分泌液",
    "此外，下一个上厕所的人需要刚好有伤口或者生殖器直接接触到了病原体，另外刚好抵抗力很低",
    "以上每一种情况，发生的概率都很低，由此可见，真正通过马桶圈发生传染的概率几乎为零",
    "蹲便也没有我们想象中的那么干净。曾有研究表明，蹲坑冲水时产生的气溶胶，细菌数量远远高于马桶",
    "这是因为蹲厕直冲式冲水，水滴飞溅范围更广，会把脏东西带得更远，而马桶一般采用虹吸式冲水，飞溅情况会好很多",
    "最好还要盖上马桶盖后再冲水",
    "上完厕所后你的手还有手机，细菌含量是马桶的17倍！一定要坚持厕所前后勤洗手",
    
    # ===== 更多逆天 =====
    "局长出去遛狗正好碰见女下属小丽也在遛狗，局长色迷迷的调侃到道：'你看我这是只公狗，你那是条母狗，它俩正好可以配对'",
    "小丽马上反击道：'可以呀，如果我的狗怀孕了，就可以说是局长那狗日的！'",
    "我妹小学没考好，刚才她在自己房间戴着耳麦玩儿qq炫舞，不一会儿就听她跟人语音，'我毕业奖金没发，没钱充q币了'",
    "'…我没有堕天使闪装不再是紫钻贵族难道你还会爱我吗？'隔了两秒压着声音都快哭了， '我们分手吧…你别傻了…没有物质的爱情就是一盘沙，都不用风吹，走两步就散了！'",
    "问：为什么中国乒乓很强大？答：因为国人面对困难善于推和挡；问：为什么中国跳水是梦之队？答：因为他们是股民；问：为什么中国射击成绩好？答：因为大家习惯睁只眼闭只眼；问：为什么中国举重成绩好？答：因为国人承受着生命不能承受之重！",
    "父亲让小明去买瓶酒，告诉他不管老板开多少一律杀一半价钱，小明点头去了。小明：这酒多少钱？老板：80。小明：不行，40。老板：60吧。小明：不行，30。老板：那就40吧。小明：不行，20。老板：30总可以了吧！小明：不行，15！老板生气了：干脆白送给你算了！小明：不行，得送两瓶。老板吐血！",
    "老婆愿意为你干点啥？韦小宝，杨过，郭靖和令狐冲几个在一起比老婆。杨过说：我老婆愿意为我跳崖。郭靖说：我老婆愿意为我和父亲决裂。令狐冲说：我老婆愿意为我被囚少林寺。韦小宝含笑不语，众人向后看，双儿已经在向黄蓉小龙女和任盈盈要电话号码和QQ号了",
    "初中文艺晚会，抢答题环节。女主持：'大家注意了，不要抢的太快。等我说完开始在举手！'然后开始念题目，说，'现在开……'这时候，一个选手就抢答了。主持人就说：'这位同学太着急了一点。我'始'(屎)还在口里，你怎么就抢了……'",
    "从前，有一栋房子里住着两户人家，一个住在楼下，一个住在楼上。有一天，楼下的在阳台上抽烟，熏得楼上的透不过气来，楼上的骂了楼下一句。楼下没脸没皮的笑着说：日照香炉生紫烟。楼上很生气，便拿了一盆洗脚水向下泼去，说：遥看瀑布挂前川~~",
    "河南人开车追尾山西人，两人下车查看，问题不大，山西人说：懒得报警了，哥们你走吧。河南人拍拍山西人的肩膀：大哥，对不起啦，缘分呐！来，我这有瓶茅台，整一口压压惊。山西人很豪爽，接过来喝了一口，又递回去：兄弟，你也来一口！河南人：别，等警察来了处理完以后我再喝",
    "古装剧里常会有这样的情节——两个武功高强的大侠比试一番，不相上下，遂化敌为友，把酒言欢抵足而眠之后更成为了莫逆之交，心中也对彼此暗生情愫，但他们知道这段感情是不被允许的，于是只能离开彼此淡化感情，道别时，他们一抱拳，发自肺腑地说：'后悔有妻！'",
    "大三男，一日上课wc，上到一半看了看四周惊觉这厕所里没有小便池误入女厕啊！当时冷汗冒的，赶紧想走人…刚提好裤子班上的几个女生就有说有笑的进来了，哥当时是神人附体啊故作惊讶的嚷了一句'你们走错了！'，接下来的一幕哥永生难忘…那些女生就这样尖叫着跑进了对面厕所…",
    
    # ===== 终极哲学2 =====
    "生活怎能缺了欢乐，天天逗你开心",
    "各种的奇葩和搞笑，要寻找快乐这是个不错的微博",
    "楼上很生气，便拿了一盆洗脚水向下泼去，说:遥看瀑布挂前川",
    "其实生活里还有不少这样让人哭笑不得的小事，不知道你有没有过",

     # ===== 更多中文猎奇 =====
    "带薪拉屎，网络流行语，最早起源于一位日本网友在推特上发表的一段话",
    "建议大家每天尽量到公司排便，因为这样占用的是工作时间，每天花10分钟的话，一年下来就是40小时，相当于积累了5天年假",
    "很多网友都表示有过相关经历，并且积极分享自己的小妙招还有与公司管理层斗智斗勇的事故",
    "马桶：你喂的有点多",
    "一次性干人家20年的量啊",
    "表情别太形象了",
    "朋友家的厕所比较认生吧",
    "嘴里默念：快下去快下去！",
    "《 捶 屎 》",
    "朋友内心是崩溃的",
    "离远点，别躺我脚上",
    "两广人震怒：为什么要用汤形容！！！",
    "男友：她出来时我得装作刚刚没听见",
    "那地毯岂不是。。。",
    "这么精准的拉法，到底经历过什么",
    "这肯定是马桶的错！！",
    "刚进去就倒了，再醒来，你们懂吗，浑身是💩啊",
    "啊啊啊，但是我还没拉完，当时管不了那么多了，就坐马桶上继续拉",
    "在一睁眼我又倒在地上，当时躺在地上缓了好久，中间又昏过去一次",
    "然后是被地面冰醒的，在这中间我隐隐约约还听见我的猫在着急的喵喵喵叫",
    "但是它又不敢靠近，可能是因为...",
    "这猫还怪讲究的",
    "婆婆那个一下子被笑死",
    "神TM刘旸哈哈哈哈哈哈哈刘旸练过肌肉，你吃不了他！！！",
    "最后那张图是不是跳喽自沙",
    "你好，打劫，笑死",
    "近日鲨雕新闻播报",
    "两个绊倒铁盒",
    "仙之人兮",
    "所以你们怎么看",
    "昨天才看到的",
    "你前二十岁真的一直吃喝玩乐吗",
    "行云流水 赏心悦目嘿四子会",
    "他这玩意用这盒装就不好吃了 就得用那白色泡沫盒 那才好吃呢",
    "往路边一蹲 今天就美好的过去了",
    "你亲眼看到了什么",
    "后面和尚掏出枪搞偷袭，理论上搞到就能做得到",
    "手撕鬼子还能说项羽在世，那你掏个那会根本没有的东西，你叮当猫啊",
    "原来是道硬菜！",
    "这种吃多了撑的视频能不能别搬来碍眼",
    "你踏马的太闲了",

]


def get_random_quote() -> str:
    """获取随机一条便秘一言（本地）"""
    return random.choice(CONSTIPATION_QUOTES)


async def get_quote_from_api(session: Optional[Any] = None) -> Optional[str]:
    """
    从 API 获取便秘一言
    
    API地址: https://api-fast.521567.xyz/api/bmyy/?type=json
    
    Args:
        session: aiohttp ClientSession，如果为None则创建临时session
        
    Returns:
        成功返回一言字符串，失败返回None
    """
    import aiohttp
    import asyncio
    
    api_url = "https://api-fast.521567.xyz/api/bmyy/?type=json"
    temp_session = None
    
    try:
        if session is None:
            temp_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))
            session = temp_session
        
        async with session.get(api_url) as response:
            response.raise_for_status()
            data = await response.json()
            
            # API 返回格式: {"text": "一言内容"}
            if isinstance(data, dict) and "text" in data:
                return data["text"]
            elif isinstance(data, str):
                return data
            else:
                return None
                
    except aiohttp.ClientResponseError as e:
        logger.debug(f"便秘一言API响应错误: {e.status}")
        return None
    except aiohttp.ClientError as e:
        logger.debug(f"便秘一言API网络错误: {e}")
        return None
    except asyncio.TimeoutError:
        logger.debug("便秘一言API请求超时")
        return None
    except Exception as e:
        logger.debug(f"便秘一言API调用失败: {e}")
        return None
    finally:
        if temp_session:
            await temp_session.close()


def get_quote_by_index(index: int) -> str:
    """根据索引获取指定一言"""
    if 0 <= index < len(CONSTIPATION_QUOTES):
        return CONSTIPATION_QUOTES[index]
    return "索引超出范围，请检查"


def get_all_quotes() -> list[str]:
    """获取所有一言"""
    return CONSTIPATION_QUOTES.copy()


def get_quotes_count() -> int:
    """获取一言总数"""
    return len(CONSTIPATION_QUOTES)
