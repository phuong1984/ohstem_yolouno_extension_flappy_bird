// definitions.js
var flappyBirdColor = '#5d2c91'; // Giữ màu giống eyeballs.py

// Block khởi tạo FlappyBird
Blockly.Blocks['flappybird_create'] = {
  init: function () {
    this.jsonInit({
      "type": "flappybird_create",
      "message0": "Khởi tạo trò chơi FlappyBird",
      "previousStatement": null,
      "nextStatement": null,
      "colour": flappyBirdColor,
      "tooltip": "Khởi tạo trò chơi FlappyBird với màn hình OLED",
      "helpUrl": ""
    });
  }
};

Blockly.Python['flappybird_create'] = function (block) {
  Blockly.Python.definitions_['import_flappybird'] = 'from flappybird import *';
  Blockly.Python.definitions_['init_flappybird'] = 'flappybird = FlappyBird()';
  return '';
};

// Block play
Blockly.Blocks['flappybird_play'] = {
  init: function () {
    this.jsonInit({
      "type": "flappybird_play",
      "message0": "Chạy trò chơi FlappyBird",
      "previousStatement": null,
      "nextStatement": null,
      "colour": flappyBirdColor,
      "tooltip": "Cập nhật và chạy trò chơi FlappyBird",
      "helpUrl": ""
    });
  }
};

Blockly.Python['flappybird_play'] = function (block) {
  return 'flappybird.play()\n';
};

// Block handle_button_pressed
Blockly.Blocks['flappybird_handle_button_pressed'] = {
  init: function () {
    this.jsonInit({
      "type": "flappybird_handle_button_pressed",
      "message0": "Xử lý nhấn nút cho FlappyBird",
      "previousStatement": null,
      "nextStatement": null,
      "colour": flappyBirdColor,
      "tooltip": "Xử lý sự kiện nhấn nút để bắt đầu, nhảy, hoặc chơi lại",
      "helpUrl": ""
    });
  }
};

Blockly.Python['flappybird_handle_button_pressed'] = function (block) {
  return 'flappybird.handle_button_pressed()\n';
};