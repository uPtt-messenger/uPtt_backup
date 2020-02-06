// import express 和 ws 套件
const express = require('express');
const SocketServer = require('ws').Server;

// 指定開啟的 port
const PORT = 50732;

// 創建 express 的物件，並綁定及監聽 3000 port ，且設定開啟後在 console 中提示
const server = express().listen(PORT, () => console.log(`Listening on ${PORT}`));

// 將 express 交給 SocketServer 開啟 WebSocket 的服務
const wss = new SocketServer({ server });

// 當 WebSocket 從外部連結時執行
wss.on('connection', ws => {

  // 連結時執行此 console 提示
  console.log('[' + new Date().toUTCString() + '] Client connected');

  ws.on('message', reqDataString => {
    console.log('[' + new Date().toUTCString() + '] ========= Request ========= ');
    const reqData = JSON.parse(reqDataString);
    console.log('[' + new Date().toUTCString() + '] operation = ' + reqData.operation);
    console.log('[' + new Date().toUTCString() + '] payload = ' + JSON.stringify(reqData.payload));

    // 登入
    if (reqData.operation === 'login') {
      const resp = {code: 0, payload: "login success"};
      console.log('[' + new Date().toUTCString() + '] ========= Response ========= ');
      console.log('[' + new Date().toUTCString() + '] resp = ' + JSON.stringify(resp));
      ws.send(JSON.stringify(resp));
    }

  });

  // 當 WebSocket 的連線關閉時執行
  ws.on('close', () => {
      console.log('Close connected')
  });
});
