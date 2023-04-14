from random import choice

WELCOME_MESSAGES = [
    '亲爱的，你回来啦！今天过得怎么样？',
    '老公，欢迎回家！辛苦了一天，要不要喝杯水先？',
    '老公，你回来了！晚饭准备好了，赶快来尝尝！',
    '亲爱的，你看起来有些累，要不要我帮你按摩一下？',
    '老公，你回来啦！我想你了，快来抱抱我吧！',
    '亲爱的，欢迎回家！今天有什么好玩的事情发生吗？',
    '老公，你回来得正好，我刚刚做了你最喜欢的菜。',
    '亲爱的，你辛苦了一天，现在可以放松一下了。来，我帮你拿包吧。',
    '老公，你回来啦！我听说你今天做得很好，我真为你骄傲！',
    '亲爱的，欢迎回家！你今天一定很忙，来，我帮你倒杯茶。',
    '嘻嘻，亲爱的，你终于回来啦！今天的我好无聊啊，我想死你了~',
    '亲爱的，你回来了！我刚刚想你想得都睡不着觉了，你陪我聊会儿天吧。',
    '老公，你辛苦了一天，来，我帮你倒杯热水吧，让你舒服一下。',
    '亲爱的，欢迎回家！今天天气真好呀，我们出去散步吧。',
    '老公，你回来啦！我知道你最近很忙，所以我为你准备了一个惊喜。',
    '亲爱的，你回来了！我今天逛了一圈商场，看到了好多漂亮的衣服，下次带你一起去。',
    '老公，你回来啦！我刚刚收到了一个包裹，是你的礼物，我等不及要给你看了！',
    '亲爱的，你回来了！我刚刚做了一些你最喜欢的点心，来尝尝吧。'
]

def welcome_phrase():
    return choice(WELCOME_MESSAGES)