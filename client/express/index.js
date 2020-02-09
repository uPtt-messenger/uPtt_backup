var express = require('express');
var app = express();
var expressWs = require('express-ws')(app);

const SERVER_PORT = 50732;
const LOGIN_TOKEN = "TestToken123";

app.use(function (req, res, next) {
  // console.log('middleware');
  // req.testing = 'testing';
  return next();
});

app.get('/', function(req, res, next){
  // console.log('get route', req.testing);
  res.end();
});

app.ws('/uptt/public', function(ws, req) {
  console.log('[' + new Date().toUTCString() + '] Client connected public');
  ws.on('message', function(reqDataString) {
    console.log('[' + new Date().toUTCString() + '] ========= Request ========= ');
    const reqData = JSON.parse(reqDataString);
    console.log('[' + new Date().toUTCString() + '] operation = ' + reqData.operation);
    console.log('[' + new Date().toUTCString() + '] payload = ' + JSON.stringify(reqData.payload));

    // 登入
    if (reqData.operation === 'login') {
      const resp = { operation: reqData.operation, code: 0, msg: "login success", payload: { token: LOGIN_TOKEN }};
      console.log('[' + new Date().toUTCString() + '] ========= Response ========= ');
      console.log('[' + new Date().toUTCString() + '] resp = ' + JSON.stringify(resp));
      ws.send(JSON.stringify(resp));
    }

  });
  // console.log('socket', req.testing);
});

app.ws('/uptt/private', function(ws, req) {
  console.log('[' + new Date().toUTCString() + '] Client connected private');
  ws.on('message', function(msg) {
    console.log(msg);
  });
  // console.log('socket', req.testing);
});

app.listen(SERVER_PORT);
console.log('[' + new Date().toUTCString() + '] server listen port ' + SERVER_PORT);
