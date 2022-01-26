import argparse
import asyncio

import requests
from aiohue import HueBridgeV2
from aiohue.v2.controllers.events import EventType
from aiohue.v2.models.button import ButtonEvent, Button

parser = argparse.ArgumentParser(description="omutsu-bot")
parser.add_argument("host", help="HueブリッジのIPアドレス")  # アプリで調べる exp.172.16.1.1
parser.add_argument("appkey", help="HueブリッジのAPPKEY")  # 調べたIPにアクセスして発行する
parser.add_argument("dimmer", help="ボタンのID")  # exp./sensors/2
parser.add_argument("slack", help="SlackのIncoming Webhook")  # 'https://hooks.slack.com/services/****'
args = parser.parse_args()

MAPPING = {
    1: "💩おむつ、おかわり❕",
    2: "🍼ミルクを飲んだよ❕",
    3: "💤ねるー",
    4: "✌️おきたー",
}

PERMITTED_DIMMER = args.dimmer.split(",")  # ["/sensors/2"]


async def main():
    while 1:
        async with HueBridgeV2(args.host, args.appkey) as bridge:
            print("イベントを受信しています...")

            def print_event(event_type, item):
                if event_type == EventType.RESOURCE_UPDATED and isinstance(item, Button):
                    if item.id_v1 in PERMITTED_DIMMER:
                        if item.button.last_event == ButtonEvent.INITIAL_PRESS:
                            message = MAPPING.get(item.metadata.control_id)
                            if message:
                                requests.post(args.slack, json={"text": message})
                                print(f"Slackに送信しました [{message}]")
                            else:
                                print(f"未定義のボタン [{item.id_v1}/{item.metadata.control_id}]")
                    else:
                        print(f"未定義のボタン [{item.id_v1}/{item.metadata.control_id}]")

            bridge.subscribe(print_event)
            await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
