import time
import threading
import traceback
import datetime

from PyPtt import PTT

import log
from errorcode import ErrorCode
from msg import Msg
from dialogue import Dialogue


class PTT_Adapter:
    def __init__(self, config_obj, command_obj):
        self.config = config_obj
        self.command = command_obj

        self.RunServer = True
        self.login = False
        self.dialog = Dialogue(self.config)

        self.bot = None

        self.thread = threading.Thread(
            target=self.run,
            daemon=True
        )
        self.thread.start()

    def logout(self):
        log.show(
            'PTTAdapter',
            log.Level.INFO,
            '執行登出'
        )

        self.bot.logout()

    def stop(self):
        log.show(
            'PTTAdapter',
            log.Level.INFO,
            '執行終止程序'
        )
        # self.logout()
        self.RunServer = False
        self.thread.join()
        log.show(
            'PTTAdapter',
            log.Level.INFO,
            '終止程序完成'
        )

    def run(self):

        log.show(
            'PTTAdapter',
            log.Level.INFO,
            '啟動'
        )

        self.bot = PTT.API(
            log_handler=self.config.PttLogHandler,
            log_level=self.config.PttLogLevel
        )

        while self.RunServer:

            # 快速反應區
            start_time = end_time = time.time()
            while end_time - start_time < self.config.QueryCycle:

                ptt_id, password = self.command.recvlogin()
                if (ptt_id, password) != (None, None):
                    log.show(
                        'PTTAdapter',
                        log.Level.INFO,
                        '執行登入'
                    )
                    try:
                        self.bot.login(
                            ptt_id,
                            password,
                            kick_other_login=True
                        )

                        self.config.initUser(ptt_id)
                        # self.dialog.loadDialogue()

                        self.login = True
                        self.bot.set_call_status(PTT.data_type.call_status.OFF)

                        res_msg = Msg(
                            operate=Msg.key_login,
                            code=ErrorCode.Success,
                            msg='登入成功'
                        )

                    except PTT.exceptions.LoginError:
                        res_msg = Msg(
                            operate=Msg.key_login,
                            code=ErrorCode.LoginFail,
                            msg='登入失敗'
                        )
                    except PTT.exceptions.WrongIDorPassword:
                        res_msg = Msg(
                            operate=Msg.key_login,
                            code=ErrorCode.LoginFail,
                            msg='帳號密碼錯誤'
                        )
                    except PTT.exceptions.LoginTooOften:
                        res_msg = Msg(
                            operate=Msg.key_login,
                            code=ErrorCode.LoginFail,
                            msg='請稍等一下再登入'
                        )
                    self.command.push(res_msg)

                if self.login:

                    if self.command.recvlogout():
                        self.login = False
                        self.logout()

                        res_msg = Msg(
                            operate=Msg.key_logout,
                            code=ErrorCode.Success,
                            msg='登出成功'
                        )

                        self.command.push(res_msg)

                    target_id, waterball_content = self.command.sendWaterBall()
                    if (target_id, waterball_content) != (None, None):
                        try:
                            self.bot.throw_waterball(target_id, waterball_content)
                            self.dialog.send(target_id, waterball_content)

                            res_msg = Msg(
                                operate=Msg.key_sendwaterball,
                                code=ErrorCode.Success,
                                msg='丟水球成功'
                            )
                        except PTT.exceptions.NoSuchUser:
                            res_msg = Msg(
                                operate=Msg.key_sendwaterball,
                                code=ErrorCode.NoSuchUser,
                                msg='無此使用者'
                            )
                        except PTT.exceptions.UserOffline:
                            res_msg = Msg(
                                operate=Msg.key_sendwaterball,
                                code=ErrorCode.UserOffLine,
                                msg='使用者離線'
                            )
                        self.command.push(res_msg)

                    # addfriend_id = self.command.addfriend()
                    # if addfriend_id is not None:
                    #     try:
                    #         user = self.bot.getUser(addfriend_id)
                    #
                    #         res_msg = Msg(
                    #             ErrorCode.Success,
                    #             '新增成功'
                    #         )
                    #
                    #     except PTT.exceptions.NoSuchUser:
                    #         print('無此使用者')

                time.sleep(0.05)
                end_time = time.time()

            # 慢速輪巡區
            log.show(
                'PTTAdapter',
                log.Level.INFO,
                '慢速輪巡'
            )

            if not self.login:
                continue

            waterball_list = self.bot.get_waterball(
                PTT.data_type.waterball_operate_type.CLEAR
            )

            if waterball_list is not None:
                for waterball in waterball_list:
                    if not waterball.type == PTT.data_type.waterball_type.CATCH:
                        continue

                    waterball_target = waterball.target
                    waterball_content = waterball.content
                    waterball_date = waterball.date

                    log.showvalue(
                        'PTTAdapter',
                        log.Level.INFO,
                        f'收到來自 {waterball_target} 的水球',
                        f'[{waterball_content}][{waterball_date}]'
                    )

                    # 01/07/2020 10:46:51
                    # 02/24/2020 15:40:34
                    date_part1 = waterball_date.split(' ')[0]
                    date_part2 = waterball_date.split(' ')[1]

                    year = int(date_part1.split('/')[2])
                    month = int(date_part1.split('/')[0])
                    day = int(date_part1.split('/')[1])

                    hour = int(date_part2.split(':')[0])
                    minute = int(date_part2.split(':')[1])
                    sec = int(date_part2.split(':')[2])

                    # print(f'waterball_date {waterball_date}')
                    # print(f'year {year}')
                    # print(f'month {month}')
                    # print(f'day {day}')
                    # print(f'hour {hour}')
                    # print(f'minute {minute}')
                    # print(f'sec {sec}')

                    waterball_timestamp = int(datetime.datetime(year, month, day, hour, minute, sec).timestamp())
                    # print(f'waterball_timestamp {waterball_timestamp}')

                    payload = Msg()
                    payload.add(Msg.key_ptt_id, waterball_target)
                    payload.add(Msg.key_content, waterball_content)
                    payload.add(Msg.key_timestamp, waterball_timestamp)

                    push_msg = Msg(
                        operate=Msg.key_recvwaterball
                    )
                    push_msg.add(Msg.key_payload, payload)

                    # self.dialog.recv(waterball_target, waterball_content, waterball_date)

                    self.command.push(push_msg)

            new_mail = self.bot.has_new_mail()
            if new_mail > 0:
                push_msg = Msg(
                    operate=Msg.key_notify)
                push_msg.add(Msg.key_msg, f'您有 {new_mail} 封新信')

                self.command.push(push_msg)
        self.logout()
