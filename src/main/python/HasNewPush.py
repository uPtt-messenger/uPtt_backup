import sys
import os
import json
import PTTLibrary
from PTTLibrary import PTT

class hasNewPush(object):
    def __init__(self, board, AID):
        self.board = board
        self.AID = AID

    def read(self, board, AID):
        try:
            filetext = self.board + '_' + self.AID + '.txt'
            file = open( filetext, 'r')
            read = file.read()
            value=int(read)
            file.close()
            return value
        except FileNotFoundError:
            print("找不到存取的紀錄檔案")
            return False

    def save(self, count):
        filetext = self.board + '_' + self.AID + '.txt'
        file = open( filetext, 'w')
        file.write(str(count))
        file.close()

    def GetPost(self, board, AID):
        global TestPostList
        TestPostList = [ (self.board, self.AID)]

        Query = False

        for (Board, Index) in TestPostList:
            try:
                if isinstance(Index, int):
                    Post = PTTBot.getPost(
                        Board,
                        PostIndex=Index,
                        Query=Query,
                    )
                else:
                    Post = PTTBot.getPost(
                        Board,
                        PostAID=Index,
                        Query=Query,
                    )
                if Post is None:
                    print('Empty')
                    continue

                if not Post.isFormatCheck():
                    print('文章格式錯誤')
                    continue

                if Post.isLock():
                    print('鎖文狀態')
                    continue
                
                if not Query:
                    TotalCount = 0
                    for Push in Post.getPushList():
                            TotalCount += 1
                    return TotalCount

            except Exception as e:
                traceback.print_tb(e.__traceback__)
                print(e)

    def compare(self):
        Count = self.GetPost(self.board, self.AID)
        print ( f'偵測到目前推文數 Count= {Count}')
        read_ = self.read(self.board, self.AID)
        print ( f'從暫存記錄檔紀錄數量為 read_ = {read_}')
        # 假設第一次追蹤此文章
        if( read_ == False ):
            self.save(Count)
        else:
            if ( Count > read_ ):
                print("偵測到的推文數 > 暫存檔案的推文數")
                self.save(Count)
                print("更新暫存檔案內容")
                return True
            else: 
                print("偵測到的推文數 <= 暫存檔案的推文數")
                return False

