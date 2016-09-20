
/* @file lang/zh_cn.js
 * @date 2016.08.11 17:00:19 
 */
(function($){
	$.lang = {
		language: 'zh_cn',
		robot_name: '\u673a\u5668\u4eba',
		robot_question_tip: '\u56de\u590d\u5e8f\u53f7\u5373\u53ef\u5f97\u5230\u5bf9\u5e94\u95ee\u9898\u7684\u7b54\u6848',
		chat_title_ext: '(\u5c0f\u80fd\u8bd5\u7528\u7248)',
		chat_xiaoneng_version: '\u5c0f\u80fd\u79d1\u6280',
		chat_button_close: '\u5173\u95ed',
		chat_button_min: '\u6700\u5c0f\u5316',
		chat_button_resize_max: '\u6269\u5927',
		chat_button_resize_min: '\u7f29\u5c0f',
		chat_button_send: '\u53d1\u9001',
		chat_button_audio: '\u6309\u4f4f\u8bf4\u8bdd',	//按住说话
		chat_button_audio_end: '\u6b63\u5728\u5f55\u97f3\u2026\u2026',
		chat_button_audio_fingerup: '\u624b\u6307\u4e0a\u6ed1\uff0c\u53d6\u6d88\u53d1\u9001', //手指上滑，取消发送
		chat_button_audio_freefinger: '\u677e\u5f00\u624b\u6307\uff0c\u53d6\u6d88\u53d1\u9001', //松开手指，取消发送
		chat_button_audio_shorttime: '\u8bf4\u8bdd\u65f6\u95f4\u592a\u77ed', //说话时间太短
		chat_button_audio_error: '\u9ea6\u514b\u98ce\u65e0\u6cd5\u4f7f\u7528', //麦克风无法使用
		chat_info_loading: '\u6b63\u5728\u52a0\u8f7d...',
		chat_info_failure: '\u52a0\u8f7d\u5931\u8d25',
		chat_info_reload: '\u91cd\u65b0\u52a0\u8f7d',
		chat_show_website: '\u67e5\u770b\u7f51\u9875',
		message_upload_failure: '\u9644\u4ef6\u4e0a\u4f20\u5931\u8d25!',
		message_button_submit: '\u63d0\u4ea4',
		evaluation_button_submit: '\u8bc4\u4ef7',
		evaluation_button_cancel: '\u53d6\u6d88',
		rightlabel: {
			about: {title:'\u5173\u4e8e\u4f01\u4e1a',selected:true},
			faq: {title:'\u5e38\u89c1\u95ee\u9898',selected:false}
		},
		goodsinfo: {
			marketprice:"\u5e02\u573a\u4ef7",
			siteprice:	"\u9500\u552e\u4ef7",
			score:		"\u597d\u8bc4\u7387",
			sizelist:	"\u5c3a\u3000\u7801",
			colorlist:	"\u989c\u3000\u8272"
		},
		toolbar_default_text: '\u65b0\u4f1a\u8bdd',
		toolbar_min_title: '{$destname}',
		toolbar_min_news: '\u60a8\u6709 {$count} \u6761\u672a\u8bfb\u6d88\u606f',
		system_title_news: '{$name}\u5ba2\u670d\u4e3a\u60a8\u670d\u52a1',
		system_first_news: '\u60a8\u597d\uff0c\u6b22\u8fce\u5149\u4e34{$name}\uff0c\u8bf7\u95ee\u6709\u4ec0\u4e48\u53ef\u4ee5\u5e2e\u60a8\uff1f',
		system_merge_session: '\u60a8\u5df2\u6253\u5f00\u540c\u4e00\u5ba2\u670d {$destname} \u7684\u4f1a\u8bdd\uff0c\u4f1a\u8bdd\u5df2\u5408\u5e76',
		system_allocation_service: '\u6b63\u5728\u4e3a\u60a8\u5206\u914d\u5ba2\u670d\uff0c\u8bf7\u7a0d\u7b49...',
		system_queue1: '\u60a8\u5f53\u524d\u6392\u961f\u4e2d\uff0c\u60a8\u6392\u5728\u7b2c{$count}\u4f4d\u3002{$br}\u5982\u679c\u4e0d\u60f3\u7b49\u5f85\uff0c\u8bf7[link message={$settingid} source=2]\u3010\u7559\u8a00\u3011[/link]\uff0c\u6211\u4eec\u4f1a\u5c3d\u5feb\u8054\u7cfb\u60a8\uff01',
		system_mobile_queue1: '\u62b1\u6b49\uff0c\u54a8\u8be2\u4eba\u6570\u8fc7\u591a\u60a8\u6392\u5728\u7b2c{$count}\u4f4d\u0020\u0020\u000d\u000a[link message={$settingid} source=2]  \u70b9\u51fb\u7559\u8a00[/link]',
		system_queue2: '\u60a8\u5f53\u524d\u6392\u961f\u4e2d\uff0c\u60a8\u6392\u5728\u7b2c{$count}\u4f4d\u3002',
		system_mobile_queue2: '\u62b1\u6b49\uff0c\u54a8\u8be2\u4eba\u6570\u8fc7\u591a\u60a8\u6392\u5728\u7b2c{$count}\u4f4d\u0020\u0020\u000d\u000a',
		system_robot_queue1: '\u60a8\u5f53\u524d\u6392\u961f\u4e2d\uff0c\u60a8\u6392\u5728\u7b2c{$count}\u4f4d\u3002{$br}\u5982\u679c\u4e0d\u60f3\u7b49\u5f85\uff0c\u8bf7[link robot]\u3010\u7ee7\u7eed\u548c\u673a\u5668\u4eba\u3011[/link]\u4f1a\u8bdd\u8fd8\u662f[link message={$settingid} source=2]\u3010\u7559\u8a00\u3011[/link]\uff0c\u6211\u4eec\u4f1a\u5c3d\u5feb\u8054\u7cfb\u60a8\uff01',
		system_robot_queue2: '\u60a8\u5f53\u524d\u6392\u961f\u4e2d\uff0c\u60a8\u6392\u5728\u7b2c{$count}\u4f4d\u3002{$br}\u5982\u679c\u4e0d\u60f3\u7b49\u5f85\uff0c\u53ef\u4ee5[link robot]\u3010\u7ee7\u7eed\u548c\u673a\u5668\u4eba\u3011[/link]\u4f1a\u8bdd\uff0c\u7a0d\u540e\u5728\u8f6c\u4eba\u5de5\u5ba2\u670d\u3002',
		system_robot_offline1: '\u4eba\u5de5\u5ba2\u670d\u90fd\u4e0d\u5728\u7ebf\uff0c\u662f[link robot]\u3010\u7ee7\u7eed\u548c\u673a\u5668\u4eba\u3011[/link]\u4f1a\u8bdd\u8fd8\u662f[link message={$settingid} source=2]\u3010\u7559\u8a00\u3011[/link]',
		system_robot_offline2: '\u4eba\u5de5\u5ba2\u670d\u90fd\u4e0d\u5728\u7ebf\uff0c\u53ef\u4ee5[link robot]\u3010\u7ee7\u7eed\u548c\u673a\u5668\u4eba\u3011[/link]\u4f1a\u8bdd\uff0c\u7a0d\u540e\u5728\u8f6c\u4eba\u5de5\u5ba2\u670d',
		system_to_robot: '[link robot]\u3010\u8f6c\u673a\u5668\u4eba\u3011[/link]',
		system_to_artificial: '\u5df2\u6210\u529f\u8f6c\u4eba\u5de5\u5ba2\u670d',
		system_no_user: '\u5f53\u524d\u5ba2\u670d\u4e0d\u5b58\u5728\u6216\u63a5\u5f85\u7ec4\u4e2d\u672a\u914d\u7f6e\u5ba2\u670d\uff01',
		system_online: '\u5ba2\u670d {$destname} \u5f88\u9ad8\u5174\u4e3a\u60a8\u670d\u52a1\uff01',
		system_offline:'\u5ba2\u670d {$destname} \u5df2\u79bb\u7ebf,\u8bf7 [link message={$settingid} source=4]\u3010\u7559\u8a00\u3011[/link]',
		system_abnormal: '\u56e0\u8fde\u7ebf\u5f02\u5e38\uff0c\u6b63\u5728\u5c1d\u8bd5\u91cd\u8fde\u3002\u82e5\u4e0d\u60f3\u7b49\u5f85\uff0c\u8bf7[link message={$settingid} source=3]\u3010\u7559\u8a00\u3011[/link]\uff0c\u6211\u4eec\u4f1a\u5c3d\u5feb\u56de\u590d\u60a8\u3002',
		system_failure: '\u60a8\u7684\u8fde\u7ebf\u5df2\u4e2d\u65ad,\u8bf7 [link reconnect={$settingid}]\u3010\u91cd\u8bd5\u3011[/link]',
		system_connect_timeout: '\u8fde\u63a5\u670d\u52a1\u5668\u8d85\u65f6\uff0c\u5efa\u8bae\u68c0\u67e5\u7f51\u7edc\u73af\u5883\u3002',
		system_connect_wait: '\u5f53\u524d\u7f51\u7edc\u4e0d\u7a33\u5b9a\uff0c\u6b63\u5728\u91cd\u8fde\u670d\u52a1\u5668\u3002',
		system_change_session: '\u5ba2\u670d {$destname} \u7ee7\u7eed\u4e3a\u60a8\u670d\u52a1',
		system_add_session: '\u5ba2\u670d {$destname} \u52a0\u5165\u5f53\u524d\u4f1a\u8bdd',
		system_switch_session: '\u60a8\u5df2\u66f4\u6362\u5ba2\u670d\uff0c{$destname}\u5ba2\u670d\u6b63\u4e3a\u60a8\u670d\u52a1\uff01',
		system_go_away_session: '\u5ba2\u670d {$destname} \u79bb\u5f00\u5f53\u524d\u4f1a\u8bdd',
		system_auto_disconnect: '\u60a8\u592a\u957f\u65f6\u95f4\u672a\u53d1\u8a00\uff0c\u7cfb\u7edf\u5df2\u81ea\u52a8\u65ad\u5f00\u8fde\u63a5\u3002',
		system_end_session: '\u4f1a\u8bdd\u5df2\u7ed3\u675f',
		system_before_evaluation: '\u60a8\u8fd8\u6ca1\u6709\u5bf9\u5ba2\u670d\u670d\u52a1\u8fdb\u884c\u8bc4\u4ef7\uff0c\u786e\u5b9a\u79bb\u5f00\u5f53\u524d\u9875\u9762\u5417\uff1f',
		system_evaluation: '\u60a8\u7684\u8bc4\u4ef7\u201c{$evaluation}\u201d\u5df2\u7ecf\u63d0\u4ea4\u3002',
		system_evaluation_failure: '\u60a8\u7684\u8bc4\u4ef7\u63d0\u4ea4\u5931\u8d25\uff01',
		system_mobile_evaluation: '\u6d88\u606f\u63d0\u793a\uff1a\u611f\u8c22\u60a8\u7684\u8bc4\u4ef7',
		system_fast_messaging: '\u60a8\u53d1\u9001\u6d88\u606f\u592a\u5feb\u4e86\uff0c\u8bf7\u4f11\u606f\u4e00\u4e0b\u3002',
		system_send_failure: '\u6d88\u606f\u53d1\u9001\u5931\u8d25\uff01[link href=javascript:void(0);]\u91cd\u65b0\u53d1\u9001[/link]',
		system_send_timeout: '\u8fde\u63a5\u8d85\u65f6\uff0c\u53d1\u9001\u6d88\u606f\u5931\u8d25',
		system_no_free_user: '\u5f53\u524d\u6ca1\u6709\u53ef\u4ee5\u66f4\u6362\u7684\u5ba2\u670d',
		system_over_rechatnum: '\u8d85\u8fc7\u53ef\u66f4\u6362\u5ba2\u670d\u6b21\u6570',
		system_upload_compress: '\u6b63\u5728\u538b\u7f29',	//正在压缩
		system_upload_start: '\u6b63\u5728\u4e0a\u4f20', //正在上传
		system_picture_error_type: '\u56fe\u7247\u7c7b\u578b\u6709\u8bef', //图片类型有误
		system_picture_error_size: '\u56fe\u7247\u592a\u5927', //图片太大
		system_giveup_wait: '\u60a8\u662f\u5426\u653e\u5f03\u6392\u961f\uff1f', //您是否放弃排队？
		system_giveup_submit: '\u786e\u8ba4', //确认
		system_no_prev_picture: '\u6ca1\u6709\u4e0a\u4e00\u5f20\u56fe\u7247', //没有上一张图片
		system_no_next_picture: '\u6ca1\u6709\u4e0b\u4e00\u5f20\u56fe\u7247', //没有下一张图片
		system_leave_message: '\u7559\u8a00', //留言
		system_config_error: '\u6570\u636e\u52a0\u8f7d\u5931\u8d25\uff0c\u8bf7\u91cd\u65b0\u52a0\u8f7d', //数据加载失败，请重新加载
		system_printing: '\u6b63\u5728\u8f93\u5165', //正在输入
		system_cookie: '\u4f60\u597d\uff01\u4e3a\u4e86\u66f4\u597d\u7684\u63d0\u4f9b\u54a8\u8be2\u670d\u52a1\uff0c\u5efa\u8bae\u5728\u3010\u8bbe\u7f6e\u3011\u002d\u3010\u0073\u0061\u0066\u0061\u0072\u0069\u3011\u002d\u5173\u95ed\u3010\u963b\u6b62\u0063\u006f\u006f\u006b\u0069\u0065\u3011', //建议开启cookie
		capture_forbidden: '\u8be5\u6d4f\u89c8\u5668\u4e0d\u652f\u6301\u5b89\u88c5\u63d2\u4ef6\uff0c\u8bf7\u4f7f\u7528\u6d4f\u89c8\u5668\u81ea\u5e26\u622a\u56fe\u5de5\u5177\u6216\u5176\u4ed6\u622a\u56fe\u5de5\u5177\u3002',
		capture_reload: '\u5728\u7ebf\u5c4f\u5e55\u622a\u56fe\u63a7\u4ef6\u88ab\u6d4f\u89c8\u5668\u963b\u6b62\uff0c\u8bf7\u8bbe\u7f6e\u957f\u671f\u5141\u8bb8\u540e\u5237\u65b0\u5f53\u524d\u9875\u9762',
		capture_install: '\u5982\u679c\u60a8\u5c1a\u672a\u5b89\u88c5\u5728\u7ebf\u5c4f\u5e55\u622a\u56fe\u63a7\u4ef6\uff0c\u70b9\u786e\u5b9a\u8fdb\u884c\u5b89\u88c5\u002e\u002e\u002e\r\n\u5982\u679c\u60a8\u5df2\u7ecf\u5b89\u88c5\u8fc7\u6b64\u622a\u56fe\u63a7\u4ef6\uff0c\u5e76\u5173\u95ed\u91cd\u65b0\u6253\u5f00\u6d4f\u89c8\u5668\u3002\r\n\u4f7f\u7528\u622a\u56fe\u6309\u94ae\u65f6\uff0c\u4ecd\u51fa\u73b0\u8fd9\u6761\u63d0\u793a\uff0c\u6211\u4eec\u5bf9\u6b64\u6df1\u8868\u6b49\u610f\uff0c\u8bf7\u70b9\u51fb\u53d6\u6d88\u6309\u94ae\uff0c\u505c\u6b62\u5b89\u88c5\uff01\r\n\u622a\u56fe\u63d2\u4ef6\u5728\u6b64\u6d4f\u89c8\u5668\u4e0a\u6ca1\u6709\u5f97\u5230\u826f\u597d\u7684\u652f\u6301\uff0c\u60a8\u53ef\u4ee5\u5c1d\u8bd5\u5176\u4ed6\u6d4f\u89c8\u5668\u002e\u002e\u002e',
		capture_activex_update: '\u622a\u56fe\u63a7\u4ef6\u6709\u65b0\u7248\u672c\uff0c\u5347\u7ea7\u540e\u624d\u80fd\u4f7f\u7528\uff01\r\n\u70b9\u786e\u5b9a\u8fdb\u884c\u5347\u7ea7\uff0c\u5347\u7ea7\u65f6\u9700\u5173\u95ed\u6d4f\u89c8\u5668\u7a97\u53e3...\r\n\u5982\u679c\u60a8\u5df2\u7ecf\u5347\u7ea7\u5b89\u88c5,\u8bf7\u5173\u95ed\u540e\u91cd\u65b0\u6253\u5f00\u6d4f\u89c8\u5668...',
		capture_other_update: '\u5728\u7ebf\u5c4f\u5e55\u622a\u56fe\u63d2\u4ef6\u6709\u65b0\u7248\u672c\uff0c\u5347\u7ea7\u540e\u624d\u80fd\u4f7f\u7528\uff01\r\n\u70b9\u786e\u5b9a\u8fdb\u884c\u5347\u7ea7...',
		news_download: '\u4e0b\u8f7d',
		news_cancel_trans: '\u53d6\u6d88\u53d1\u9001',
		news_trans_success: '\u4e0a\u4f20\u6210\u529f',
		news_trans_retry: '\u91cd\u65b0\u4e0a\u4f20',
		news_trans_failure_size: '\u8bf7\u4e0a\u4f20\u5c0f\u4e8e {$maxsize}MB \u7684\u6587\u4ef6',
		news_trans_failure_type: '\u4ec5\u652f\u6301\u4e0a\u4f20\u4ee5\u4e0b\u7c7b\u578b\u7684\u6587\u4ef6\uff1a {$type} ',
		news_trans_failure: '\u4e0a\u4f20\u5931\u8d25',
		news_trans_cancel: '\u5df2\u53d6\u6d88\u53d1\u9001',
		news_trans_size: '\u6587\u4ef6\u592a\u5927',
		news_trans_type: '\u4e0d\u652f\u6301\u6b64\u7c7b\u578b\u6587\u4ef6',
		news_new: '\u65b0\u6d88\u606f',
		button_face: '\u8868\u60c5',
		button_file: '\u6587\u4ef6',
		button_image: '\u56fe\u7247',
		button_save: '\u4fdd\u5b58',
		button_view: '\u804a\u5929\u8bb0\u5f55',
		button_captureImage: '\u622a\u56fe',
		button_evaluation: '\u8bc4\u4ef7',
		button_change_csr: '\u66f4\u6362\u5ba2\u670d',
		button_switch_manual: '\u8f6c\u4eba\u5de5',
		button_more: '\u66f4\u591a',
		button_history: '\u8fd4\u56de',
		button_end_session: '\u7ed3\u675f\u4f1a\u8bdd',
		button_start_session: '\u7ee7\u7eed\u4f1a\u8bdd',
		button_enter: 'Enter',
		button_ctrl_enter: 'Ctrl+Enter',
		button_capture_show_chatWin: '\u4e0d\u9690\u85cf\u7a97\u53e3',
		button_capture_hidden_chatWin: '\u9690\u85cf\u7a97\u53e3',
		back_button_text: '\u8fd4\u56de',
		dest_sign_text: '\u4e1a\u52a1\u4ecb\u7ecd',
		default_textarea_text: '\u6211\u60f3\u95ee...',
		send_button_text: '\u53d1\u9001\u6d88\u606f',
		default_evaluation_form_title: '\u670d\u52a1\u8bc4\u4ef7',
		default_evaluation_form_fields: [
			{title:"\u8bf7\u60a8\u8bc4\u4ef7\u6211\u7684\u670d\u52a1",name:"evaluation",type:"radio",required:true,defaultText:"5",options:[
				{text:"\u975e\u5e38\u6ee1\u610f",value:"5"},
				{text:"\u6ee1\u610f",value:"4"},
				{text:"\u4e00\u822c",value:"3"},
				{text:"\u4e0d\u6ee1\u610f",value:"2"},
				{text:"\u5f88\u4e0d\u6ee1\u610f",value:"1"}
			], message:["\u8bf7\u5bf9\u5ba2\u670d\u8fdb\u884c\u8bc4\u4ef7", ""]},
			{title:"\u5efa\u8bae\u4e0e\u53cd\u9988", multipart: true,name:"proposal",type:"textarea","defaultText":"\u611f\u8c22\u60a8\u7684\u53cd\u9988\uff0c\u6211\u4eec\u4f1a\u66f4\u52a0\u52aa\u529b\u3002",required:false,max:200,message:["","","\u5efa\u8bae\u5185\u5bb9\u4e0d\u80fd\u8d85\u8fc7100\u4e2a\u4e2d\u6587\u5b57\u7b26"]}
		],
		default_message_form_fields:[
			{title:"\u59d3\u540d",name:"msg_name",type:"text","defaultText":"\u8bf7\u586b\u5199\u60a8\u7684\u771f\u5b9e\u59d3\u540d",required:true,message:["\u8bf7\u8f93\u5165\u60a8\u7684\u6635\u79f0"]},
			{title:"\u7535\u8bdd",name:"msg_tel",type:"text","defaultText":"\u8bf7\u586b\u5199\u56fa\u5b9a\u6216\u79fb\u52a8\u7535\u8bdd\u53f7\u7801",required:true,verification:"phone",message:["\u8bf7\u586b\u5199\u7535\u8bdd\u53f7\u7801","\u7535\u8bdd\u53f7\u7801\u683c\u5f0f\u9519\u8bef"]},
			{title:"\u90ae\u7bb1",name:"msg_email",type:"text","defaultText":"\u8bf7\u586b\u5199\u60a8\u7684\u90ae\u7bb1\u5730\u5740",required:false,verification:"email",message:["\u8bf7\u586b\u5199\u60a8\u7684\u90ae\u7bb1\u5730\u5740","\u7535\u5b50\u90ae\u7bb1\u5730\u5740\u683c\u5f0f\u9519\u8bef"]},
			{title:"\u7559\u8a00",name:"msg_content",type:"textarea","defaultText":"\u8bf7\u5c06\u60a8\u7684\u95ee\u9898\u8be6\u7ec6\u5199\u4e0b\uff0c\u6211\u4eec\u4f1a\u5c3d\u5feb\u4e0e\u60a8\u8054\u7cfb\u3002",required:true,max:400,message:["\u7559\u8a00\u5185\u5bb9\u4e0d\u80fd\u4e3a\u7a7a","","\u7559\u8a00\u5185\u5bb9\u4e0d\u80fd\u8d85\u8fc7200\u4e2a\u4e2d\u6587\u5b57\u7b26"]}
		],
		default_submitinfo_form_title: '',
		default_submitinfo_form_fields: [
			{title:"\u95ee\u3000\u3000\u9898",name:"tips_question",type:"text","defaultText":"",required:true,message:["\u8bf7\u8f93\u5165\u95ee\u9898\u6807\u9898"]},
			{title:"\u95ee\u9898\u7c7b\u578b",name:"tips_type",type:"select","defaultText":"-\u8bf7\u9009\u62e9\u95ee\u9898\u7c7b\u578b-",required:true, options:[
				"\u552e\u524d\u54a8\u8be2",
				"\u9000\u6362\u8d27\u670d\u52a1",
				"\u7269\u6d41\u54a8\u8be2",
				"\u7f3a\u8d27\u5efa\u8bae"
			]},
			{title:"\u5ba2\u6237\u59d3\u540d",name:"tips_name",type:"text","defaultText":"",required:false},
			{title:"\u8054\u7cfb\u7535\u8bdd",name:"tips_phone",type:"text","defaultText":"",required:false,verification:"phone"},
			{title:"\u7535\u5b50\u90ae\u4ef6",name:"tips_email",type:"text","defaultText":"",required:false,verification:"email"}
		],
		message_prompt: '\u5f53\u524d\u65e0\u5ba2\u670d\u5728\u7ebf\uff0c[link href="javascript:void(0);"]\u6211\u8981\u7559\u8a00[/link]',
		message_success: '\u7559\u8a00\u63d0\u4ea4\u6210\u529f\uff01',
		message_no_null: '*',
		message_no_null_char: '(\u5fc5\u586b)',
		editorFaceAlt: {
			'1':'wx','2':'tx','3':'hx','4':'dy','5':'ll','6':'sj','7':'dk','8':'jy','9':'zj','10':'gg',
			'11':'kx','12':'zb','13':'yw','14':'dn','15':'sh','16':'ku','17':'fn','18':'ws','19':'ok','20':'xh'
		}
	};
})(nTalk);
