"""
本地兜底数据

当 API 接口不可用时，使用本地数据作为兜底方案
"""

import random
from datetime import datetime
from typing import Optional

# 本地用户数据缓存（内存中）
_local_poop_data: dict[str, dict] = {}


def start_local_poop(user_id: str, user_name: str) -> str:
    """开始本地拉屎记录"""
    now = datetime.now()
    
    # 如果已经在拉，提示重新开始
    if user_id in _local_poop_data:
        old_start = _local_poop_data[user_id].get('start_time')
        if old_start:
            _local_poop_data[user_id] = {
                'user_name': user_name,
                'start_time': now,
                'history': _local_poop_data[user_id].get('history', [])
            }
            return f"【本地模式】{user_name} 重新开始记录！\n💪 祝您排便顺畅！"
    
    # 新记录
    _local_poop_data[user_id] = {
        'user_name': user_name,
        'start_time': now,
        'history': []
    }
    
    # 随机祝福
    blessings = [
        "祝您排便顺畅，一泻千里！🚽",
        "愿您的肠道如丝般顺滑！💩",
        "祝您战况顺利，速战速决！⚡",
        "愿马桶之神保佑您！🙏",
        "祝您这次能刷新个人记录！🏆",
    ]
    
    return f"【本地模式】{user_name} 开始记录！\n{random.choice(blessings)}"


def end_local_poop(user_id: str, user_name: str) -> str:
    """结束本地拉屎记录"""
    if user_id not in _local_poop_data:
        return f"【本地模式】{user_name} 您还没有开始记录呢！发送 /拉屎 开始记录。"
    
    data = _local_poop_data[user_id]
    start_time = data.get('start_time')
    
    if not start_time:
        return f"【本地模式】{user_name} 记录异常，请重新开始！"
    
    # 计算时长
    end_time = datetime.now()
    duration = end_time - start_time
    minutes = int(duration.total_seconds() / 60)
    seconds = int(duration.total_seconds() % 60)
    
    # 保存到历史
    if 'history' not in data:
        data['history'] = []
    
    data['history'].append({
        'start_time': start_time,
        'end_time': end_time,
        'duration_seconds': duration.total_seconds()
    })
    
    # 保留最近10条记录
    data['history'] = data['history'][-10:]
    
    # 重置当前记录
    data['start_time'] = None
    
    # 根据时长给出评价
    if minutes < 1:
        evaluation = "闪电侠！这速度，肠道都不反应过来！⚡"
    elif minutes < 3:
        evaluation = "正常发挥，健康排便！👍"
    elif minutes < 5:
        evaluation = "不错不错，很顺畅嘛！💪"
    elif minutes < 10:
        evaluation = "持久战选手，肠道需要锻炼了！🏃"
    elif minutes < 20:
        evaluation = "肠道马拉松完成！建议多吃蔬菜！🥬"
    else:
        evaluation = "您这是在里面睡着了吗？💤 建议就医检查！"
    
    # 计算平均时长
    if data['history']:
        avg_duration = sum(h['duration_seconds'] for h in data['history']) / len(data['history'])
        avg_minutes = int(avg_duration / 60)
        avg_seconds = int(avg_duration % 60)
        avg_text = f"\n📊 平均时长：{avg_minutes}分{avg_seconds}秒"
    else:
        avg_text = ""
    
    return f"【本地模式】🎉 {user_name} 战斗结束！\n⏱️ 本次时长：{minutes}分{seconds}秒\n📋 评价：{evaluation}{avg_text}"


def get_local_poop_list() -> str:
    """获取本地正在拉屎的列表"""
    active_users = []
    
    for user_id, data in _local_poop_data.items():
        if data.get('start_time'):
            user_name = data.get('user_name', '未知用户')
            start_time = data['start_time']
            duration = datetime.now() - start_time
            minutes = int(duration.total_seconds() / 60)
            seconds = int(duration.total_seconds() % 60)
            active_users.append(f"🚽 {user_name} - 已战斗{minutes}分{seconds}秒")
    
    if not active_users:
        return "【本地模式】当前没有人在战斗，快来发送 /拉屎 成为第一个！"
    
    header = f"【本地模式】📊 当前有 {len(active_users)} 位勇士正在战斗！\n\n"
    return header + "\n".join(active_users)


def clear_local_data(user_id: Optional[str] = None) -> str:
    """清理本地数据"""
    global _local_poop_data
    
    if user_id:
        if user_id in _local_poop_data:
            del _local_poop_data[user_id]
            return f"已清理用户 {user_id} 的数据"
        return f"用户 {user_id} 没有数据"
    else:
        count = len(_local_poop_data)
        _local_poop_data = {}
        return f"已清理所有 {count} 位用户的数据"
