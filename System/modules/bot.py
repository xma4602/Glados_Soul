import vk_api, vk
from vk_api.bot_longpoll import VkBotLongPoll

vk_session = vk_api.VkApi(
    token='vk1.a.fW6xhIXyLDwog_FX1fRTMiyEoVZL_b0ENm2J4y5lBKZ0hefDhJylNknLzd4I72GJ6--1rNhspg41efbhbJYPX1osNLmRCi9QBKo5v2AhBszehAZKPFUCby-7EeOkHOXXl_2Cp6Z8-0Hqo3yU9FF-B5811qznwiJq-uFEq_rOmUXkHde-9RvMTvm_T4WyFFNWsCd1baqaZA1mwaB69y9TSg')
longpoll = VkBotLongPoll(vk_session, '218320118')
vk = vk_session.get_api()


def send(message: str, ids: list):
    for ID in ids:
        vk.messages.send(
            key=tuple('f25124946931a230031d57ddd73e4e0efcec4b7b'),
            server=tuple('https://lp.vk.com/wh218320118'),
            ts=tuple('42'),
            random_id=0,
            message=message,
            peer_id=int(ID),
        )