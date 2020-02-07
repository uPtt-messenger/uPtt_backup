var express = require('express');
var app = express();
var expressWs = require('express-ws')(app);

app.use(function (req, res, next) {
  console.log('middleware');
  req.testing = 'testing';
  return next();
});

app.get('/', function(req, res, next){
  console.log('get route', req.testing);
  res.end();
});

app.ws('/', function(ws, req) {
  ws.on('message', function(msg) {
    console.log(msg);
  });
  console.log('socket', req.testing);
});

app.listen(3000);




































































// 將 express 交給 SocketServer 開啟 WebSocket 的服務
// const publicWss = new SocketServer({ server: server, path: "/uptt/public" });

// // 當 WebSocket 從外部連結時執行
// publicWss.on('connection', ws => {

//   // 連結時執行此 console 提示
//   console.log('[' + new Date().toUTCString() + '] Client connected public');

//   ws.on('message', reqDataString => {
//     console.log('[' + new Date().toUTCString() + '] ========= Request ========= ');
//     const reqData = JSON.parse(reqDataString);
//     console.log('[' + new Date().toUTCString() + '] operation = ' + reqData.operation);
//     console.log('[' + new Date().toUTCString() + '] payload = ' + JSON.stringify(reqData.payload));

//     // 登入
//     if (reqData.operation === 'login') {
//       const resp = {code: 0, payload: "login success"};
//       console.log('[' + new Date().toUTCString() + '] ========= Response ========= ');
//       console.log('[' + new Date().toUTCString() + '] resp = ' + JSON.stringify(resp));
//       ws.send(JSON.stringify(resp));
//     }

//   });

//   // 當 WebSocket 的連線關閉時執行
//   ws.on('close', () => {
//       console.log('[' + new Date().toUTCString() + '] Close connected')
//   });

// });

// const privateWss = new SocketServer({ server: server, path: "/uptt/private" });
// privateWss.on('connection', ws => {

//   // 連結時執行此 console 提示
//   console.log('[' + new Date().toUTCString() + '] Client connected private');

//   // 當 WebSocket 的連線關閉時執行
//     ws.on('close', () => {
//       console.log('[' + new Date().toUTCString() + '] Close connected')
//   });
// });
