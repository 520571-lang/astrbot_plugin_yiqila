import java.net.URLEncoder;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

import android.app.Activity;
import android.app.AlertDialog;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.*;

String API_URL = "http://api-fast.521567.xyz/api/yql/";
String API_KEY = "114514";
String CONFIG_NAME = "settings";
String BLACKLIST_KEY = "group_blacklist";

// ==================== 全局变量 ====================
boolean isEnabled = true;
boolean processSelfMsg = false;  // 是否处理自己的消息，默认关闭
List<String> groupBlacklist = new java.util.ArrayList<>();

Map<String, String[]> COMMANDS = new HashMap<String, String[]>() {{
    put("拉屎", new String[]{"拉屎", "拉粑粑", "拉臭臭"});
    put("一起拉", new String[]{"一起拉", "谁在拉", "谁在拉"});
    put("拉完了", new String[]{"拉完了", "拉完", "拉完了啦", "结束拉屎"});
}};

// ==================== 初始化 ====================
void init() {
    try {
        isEnabled = getBoolean(CONFIG_NAME, "enabled", true);
        processSelfMsg = getBoolean(CONFIG_NAME, "processSelfMsg", false);
        loadBlacklist();
    } catch (Exception e) {
        isEnabled = true;
        processSelfMsg = false;
    }
}

void loadBlacklist() {
    try {
        String listStr = getString(BLACKLIST_KEY, "list", "");
        groupBlacklist.clear();
        if (listStr != null && !listStr.isEmpty()) {
            String[] groups = listStr.split(",");
            for (String g : groups) {
                if (!g.trim().isEmpty()) {
                    groupBlacklist.add(g.trim());
                }
            }
        }
    } catch (Exception e) {
    }
}

void saveBlacklist() {
    try {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < groupBlacklist.size(); i++) {
            if (i > 0) sb.append(",");
            sb.append(groupBlacklist.get(i));
        }
        putString(BLACKLIST_KEY, "list", sb.toString());
    } catch (Exception e) {
    }
}

boolean isGroupBlacklisted(String groupUin) {
    return groupBlacklist.contains(groupUin);
}

// ==================== UI辅助方法 ====================
int dp(int px, Activity act) {
    return (int)(px * act.getResources().getDisplayMetrics().density);
}

GradientDrawable cardBg(Activity act) {
    GradientDrawable gd = new GradientDrawable();
    gd.setColor(Color.parseColor("#1A1D24"));
    gd.setCornerRadius(dp(16, act));
    gd.setStroke(dp(1, act), Color.parseColor("#2A2E38"));
    return gd;
}

TextView createBtn(Activity act, String text, int color, Runnable click) {
    TextView btn = new TextView(act);
    btn.setText(text);
    btn.setTextSize(14);
    btn.setTypeface(Typeface.DEFAULT_BOLD);
    btn.setTextColor(Color.parseColor("#FFFFFF"));
    btn.setGravity(Gravity.CENTER);
    btn.setPadding(dp(20, act), dp(12, act), dp(20, act), dp(12, act));
    GradientDrawable gd = new GradientDrawable();
    gd.setColor(color);
    gd.setCornerRadius(dp(12, act));
    btn.setBackground(gd);
    if (click != null) btn.setOnClickListener(v -> click.run());
    return btn;
}

// ==================== 菜单 ====================
addItem("开关插件", "togglePlugin");
addItem("处理自己消息", "toggleProcessSelfMsg");
addItem("群黑名单", "manageGroupBlacklist");
addItem("测试连接", "testConnection");

void togglePlugin(int chatType, String peerUin, String name) {
    isEnabled = !isEnabled;
    try {
        putBoolean(CONFIG_NAME, "enabled", isEnabled);
    } catch (Exception e) {
    }
    String msg = "一起拉屎插件已" + (isEnabled ? "启用" : "禁用");
    toast(msg);
    qqToast(2, msg);
}

void toggleProcessSelfMsg(int chatType, String peerUin, String name) {
    processSelfMsg = !processSelfMsg;
    try {
        putBoolean(CONFIG_NAME, "processSelfMsg", processSelfMsg);
    } catch (Exception e) {
    }
    String msg = "处理自己消息已" + (processSelfMsg ? "开启" : "关闭");
    toast(msg);
    qqToast(2, msg);
}

// ==================== 群黑名单管理 ====================
void manageGroupBlacklist(int chatType, String peerUin, String name) {
    Activity act = getNowActivity();
    if (act == null) {
        toast("无法获取当前界面");
        return;
    }
    
    act.runOnUiThread(() -> {
        LinearLayout layout = new LinearLayout(act);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(dp(20, act), dp(20, act), dp(20, act), dp(20, act));
        layout.setBackground(cardBg(act));
        
        TextView title = new TextView(act);
        title.setText("群黑名单管理");
        title.setTextSize(18);
        title.setTypeface(Typeface.DEFAULT_BOLD);
        title.setTextColor(Color.parseColor("#FFFFFF"));
        title.setGravity(Gravity.CENTER);
        layout.addView(title);
        
        TextView desc = new TextView(act);
        desc.setText("黑名单中的群不会响应拉屎功能\n当前黑名单群数: " + groupBlacklist.size());
        desc.setTextSize(12);
        desc.setTextColor(Color.parseColor("#8E9AAB"));
        desc.setGravity(Gravity.CENTER);
        desc.setPadding(0, dp(8, act), 0, dp(16, act));
        layout.addView(desc);
        
        // 显示当前黑名单
        ScrollView scroll = new ScrollView(act);
        TextView listView = new TextView(act);
        updateBlacklistDisplay(listView);
        listView.setTextSize(13);
        listView.setTextColor(Color.parseColor("#8E9AAB"));
        listView.setPadding(dp(12, act), dp(12, act), dp(12, act), dp(12, act));
        listView.setBackgroundColor(Color.parseColor("#0F1115"));
        scroll.addView(listView);
        layout.addView(scroll, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(150, act)));
        
        // 按钮行
        LinearLayout btnRow = new LinearLayout(act);
        btnRow.setOrientation(LinearLayout.HORIZONTAL);
        btnRow.setPadding(0, dp(16, act), 0, 0);
        
        btnRow.addView(createBtn(act, "添加当前群", Color.parseColor("#4CAF50"), () -> {
            if (chatType != 2) {
                toast("仅在群聊中可用");
                return;
            }
            if (groupBlacklist.contains(peerUin)) {
                toast("该群已在黑名单中");
                return;
            }
            groupBlacklist.add(peerUin);
            saveBlacklist();
            updateBlacklistDisplay(listView);
            desc.setText("黑名单中的群不会响应拉屎功能\n当前黑名单群数: " + groupBlacklist.size());
            toast("已添加当前群到黑名单");
        }));
        
        btnRow.addView(createBtn(act, "手动添加", Color.parseColor("#2196F3"), () -> {
            showAddGroupDialog(act, listView, desc);
        }));
        
        btnRow.addView(createBtn(act, "删除群", Color.parseColor("#F44336"), () -> {
            if (groupBlacklist.isEmpty()) {
                toast("黑名单为空");
                return;
            }
            showRemoveGroupDialog(act, listView, desc);
        }));
        
        LinearLayout.LayoutParams btnParams = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1);
        btnParams.setMargins(dp(4, act), 0, dp(4, act), 0);
        for (int i = 0; i < btnRow.getChildCount(); i++) {
            btnRow.getChildAt(i).setLayoutParams(btnParams);
        }
        layout.addView(btnRow);
        
        // 清空按钮
        TextView clearBtn = createBtn(act, "清空黑名单", Color.parseColor("#FF9800"), () -> {
            new AlertDialog.Builder(act)
                .setTitle("确认清空")
                .setMessage("确定要清空所有黑名单群吗？")
                .setPositiveButton("确定", (d, w) -> {
                    groupBlacklist.clear();
                    saveBlacklist();
                    updateBlacklistDisplay(listView);
                    desc.setText("黑名单中的群不会响应拉屎功能\n当前黑名单群数: 0");
                    toast("黑名单已清空");
                })
                .setNegativeButton("取消", null)
                .show();
        });
        LinearLayout.LayoutParams clearParams = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        clearParams.setMargins(0, dp(8, act), 0, 0);
        clearBtn.setLayoutParams(clearParams);
        layout.addView(clearBtn);
        
        AlertDialog dialog = new AlertDialog.Builder(act).create();
        dialog.setView(layout);
        dialog.show();
        Window win = dialog.getWindow();
        if (win != null) {
            win.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
            win.setLayout(dp(340, act), ViewGroup.LayoutParams.WRAP_CONTENT);
        }
    });
}

void updateBlacklistDisplay(TextView tv) {
    if (groupBlacklist.isEmpty()) {
        tv.setText("暂无黑名单群");
    } else {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < groupBlacklist.size(); i++) {
            sb.append(i + 1).append(". ").append(groupBlacklist.get(i)).append("\n");
        }
        tv.setText(sb.toString().trim());
    }
}

void showAddGroupDialog(Activity act, TextView listView, TextView desc) {
    LinearLayout layout = new LinearLayout(act);
    layout.setOrientation(LinearLayout.VERTICAL);
    layout.setPadding(dp(20, act), dp(20, act), dp(20, act), dp(20, act));
    layout.setBackground(cardBg(act));
    
    TextView title = new TextView(act);
    title.setText("添加群到黑名单");
    title.setTextSize(18);
    title.setTypeface(Typeface.DEFAULT_BOLD);
    title.setTextColor(Color.parseColor("#FFFFFF"));
    title.setGravity(Gravity.CENTER);
    layout.addView(title);
    
    EditText input = new EditText(act);
    input.setHint("请输入群号");
    input.setTextColor(Color.WHITE);
    input.setHintTextColor(Color.parseColor("#8E9AAB"));
    input.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
    input.setBackgroundColor(Color.parseColor("#2A2E38"));
    input.setPadding(dp(16, act), dp(12, act), dp(16, act), dp(12, act));
    LinearLayout.LayoutParams inputParams = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    inputParams.setMargins(0, dp(16, act), 0, dp(16, act));
    layout.addView(input, inputParams);
    
    LinearLayout btnRow = new LinearLayout(act);
    btnRow.setOrientation(LinearLayout.HORIZONTAL);
    
    btnRow.addView(createBtn(act, "确定", Color.parseColor("#4CAF50"), () -> {
        String groupUin = input.getText().toString().trim();
        if (groupUin.isEmpty()) {
            toast("群号不能为空");
            return;
        }
        if (groupBlacklist.contains(groupUin)) {
            toast("该群已在黑名单中");
            return;
        }
        groupBlacklist.add(groupUin);
        saveBlacklist();
        updateBlacklistDisplay(listView);
        desc.setText("黑名单中的群不会响应拉屎功能\n当前黑名单群数: " + groupBlacklist.size());
        toast("已添加群 " + groupUin + " 到黑名单");
    }));
    
    btnRow.addView(createBtn(act, "取消", Color.parseColor("#F44336"), () -> {}));
    
    LinearLayout.LayoutParams btnParams = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1);
    btnParams.setMargins(dp(4, act), 0, dp(4, act), 0);
    for (int i = 0; i < btnRow.getChildCount(); i++) {
        btnRow.getChildAt(i).setLayoutParams(btnParams);
    }
    layout.addView(btnRow);
    
    AlertDialog dialog = new AlertDialog.Builder(act).create();
    dialog.setView(layout);
    dialog.show();
    Window win = dialog.getWindow();
    if (win != null) {
        win.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        win.setLayout(dp(300, act), ViewGroup.LayoutParams.WRAP_CONTENT);
    }
}

void showRemoveGroupDialog(Activity act, TextView listView, TextView desc) {
    String[] items = groupBlacklist.toArray(new String[0]);
    new AlertDialog.Builder(act)
        .setTitle("选择要删除的群")
        .setItems(items, (d, w) -> {
            String removed = groupBlacklist.remove(w);
            saveBlacklist();
            updateBlacklistDisplay(listView);
            desc.setText("黑名单中的群不会响应拉屎功能\n当前黑名单群数: " + groupBlacklist.size());
            toast("已删除群 " + removed);
        })
        .show();
}

void testConnection(int chatType, String peerUin, String name) {
    final int type = chatType;
    final String uin = peerUin;
    new Thread(() -> {
        try {
            String testUrl = API_URL + "?key=" + URLEncoder.encode(API_KEY, "UTF-8") 
                + "&action=一起拉&qq=12345&nickname=测试用户";
            
            URL url = new URL(testUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(5000);
            
            int responseCode = conn.getResponseCode();
            
            BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            reader.close();
            conn.disconnect();
            
            String result = response.toString();
            String msg = "API测试成功！\n码: " + responseCode + "\n内容: " + result.substring(0, Math.min(100, result.length()));
            sendMsg(uin, msg, type);
            qqToast(2, "连接成功");
        } catch (Exception e) {
            String error = "API测试失败: " + e.getMessage();
            sendMsg(uin, error, type);
            qqToast(1, "连接失败");
        }
    }).start();
}

// ==================== 命令匹配 ====================
String matchCommand(String msg) {
    for (Map.Entry<String, String[]> entry : COMMANDS.entrySet()) {
        for (String cmd : entry.getValue()) {
            if (msg.equals(cmd) || msg.startsWith(cmd + " ") || msg.startsWith(cmd + "　")) {
                return entry.getKey();
            }
        }
    }
    return null;
}

// ==================== 获取昵称 ====================
String getNickname(int chatType, String peerUin, String userUin) {
    try {
        if (chatType == 2) {
            Object memberInfo = getMemberInfo(peerUin, userUin);
            if (memberInfo != null) {
                String uinName = memberInfo.uinName;
                if (uinName != null && !uinName.isEmpty()) {
                    return uinName;
                }
            }
        }
        
        List<?> friends = getAllFriend();
        if (friends != null) {
            for (Object friend : friends) {
                if (friend.uin != null && friend.uin.equals(userUin)) {
                    if (friend.remark != null && !friend.remark.isEmpty()) {
                        return friend.remark;
                    }
                    if (friend.name != null && !friend.name.isEmpty()) {
                        return friend.name;
                    }
                }
            }
        }
    } catch (Exception e) {
    }
    return "匿名用户";
}

// ==================== API调用 ====================
String callApi(String action, String qq, String nickname, boolean showQQ) {
    return callApi(action, qq, nickname, showQQ, "text");
}

String callApi(String action, String qq, String nickname, boolean showQQ, String format) {
    try {
        String urlStr = API_URL + "?key=" + URLEncoder.encode(API_KEY, "UTF-8") 
            + "&action=" + URLEncoder.encode(action, "UTF-8")
            + "&qq=" + URLEncoder.encode(qq, "UTF-8")
            + "&nickname=" + URLEncoder.encode(nickname, "UTF-8");
        
        if (showQQ) urlStr += "&qqtrue=true";
        if (format != null && !format.equals("text")) {
            urlStr += "&format=" + format;
        }
        
        URL url = new URL(urlStr);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setConnectTimeout(5000);
        conn.setReadTimeout(5000);
        
        int code = conn.getResponseCode();
        
        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) sb.append(line);
        reader.close();
        conn.disconnect();
        
        String result = sb.toString();
        return result;
    } catch (Exception e) {
        return null;
    }
}

// 从API响应中提取图片URL
String extractImageUrl(String apiResponse) {
    if (apiResponse == null) return null;
    
    int idx = apiResponse.indexOf("\"image_url\":\"");
    if (idx != -1) {
        int start = idx + 13;
        int end = apiResponse.indexOf("\"", start);
        if (end > start) {
            String url = apiResponse.substring(start, end);
            return url;
        }
    }
    return null;
}

String extractMessage(String apiResponse) {
    if (apiResponse == null) return "接口调用失败";
    
    int idx = apiResponse.indexOf("\"message\":\"");
    if (idx != -1) {
        int start = idx + 11;
        int end = apiResponse.indexOf("\",\"", start);
        if (end == -1) end = apiResponse.indexOf("\"}", start);
        if (end > start) return apiResponse.substring(start, end);
    }
    return apiResponse;
}

// 从API响应中提取列表数据
List<Map<String, String>> extractListData(String apiResponse) {
    List<Map<String, String>> list = new java.util.ArrayList<>();
    if (apiResponse == null) return list;
    
    try {
        int dataIdx = apiResponse.indexOf("\"data\":");
        if (dataIdx == -1) {
            return list;
        }
        
        int listIdx = apiResponse.indexOf("\"list\":", dataIdx);
        if (listIdx == -1) {
            return list;
        }
        
        int arrStart = apiResponse.indexOf("[", listIdx);
        int arrEnd = apiResponse.indexOf("]", arrStart);
        if (arrStart == -1 || arrEnd == -1) {
            return list;
        }
        
        String arrContent = apiResponse.substring(arrStart + 1, arrEnd).trim();
        
        if (arrContent.isEmpty()) {
            return list;
        }
        
        String[] items = arrContent.split("\\},\\s*\\{");
        for (String item : items) {
            item = item.trim();
            if (item.isEmpty()) continue;
            if (item.startsWith("{")) item = item.substring(1);
            if (item.endsWith("}")) item = item.substring(0, item.length() - 1);
            
            Map<String, String> map = new HashMap<>();
            int nameIdx = item.indexOf("\"nickname\":\"");
            if (nameIdx != -1) {
                int ns = nameIdx + 13;
                int ne = item.indexOf("\"", ns);
                if (ne > ns) {
                    String nickname = item.substring(ns, ne);
                    map.put("nickname", nickname);
                }
            }
            int qqIdx = item.indexOf("\"qq\":\"");
            if (qqIdx != -1) {
                int qs = qqIdx + 7;
                int qe = item.indexOf("\"", qs);
                if (qe > qs) map.put("qq", item.substring(qs, qe));
            }
            if (!map.isEmpty()) list.add(map);
        }
    } catch (Exception e) {
        e.printStackTrace();
    }
    return list;
}

// ==================== 图片生成与发送 ====================
// 生成名单图片并发送
void sendPoopListAsImage(String peerUin, int chatType, List<Map<String, String>> userList, String title) {
    try {
        Activity act = getNowActivity();
        if (act == null) {
            sendMsg(peerUin, title, chatType);
            return;
        }
        
        act.runOnUiThread(() -> {
            try {
                int width = 800;
                int itemHeight = 100;
                int headerHeight = 120;
                int footerHeight = 60;
                int height = headerHeight + (userList.size() * itemHeight) + footerHeight;
                
                android.graphics.Bitmap bitmap = android.graphics.Bitmap.createBitmap(width, height, android.graphics.Bitmap.Config.ARGB_8888);
                android.graphics.Canvas canvas = new android.graphics.Canvas(bitmap);
                
                canvas.drawColor(Color.parseColor("#FFF8E7"));
                
                android.graphics.Paint paint = new android.graphics.Paint();
                paint.setAntiAlias(true);
                
                paint.setColor(Color.parseColor("#8B4513"));
                canvas.drawRect(0, 0, width, headerHeight, paint);
                
                paint.setColor(Color.WHITE);
                paint.setTextSize(48);
                paint.setTypeface(Typeface.DEFAULT_BOLD);
                paint.setTextAlign(android.graphics.Paint.Align.CENTER);
                canvas.drawText("🚽 一起拉屎名单", width / 2, headerHeight / 2 + 16, paint);
                
                paint.setTextSize(28);
                paint.setColor(Color.parseColor("#FFE4B5"));
                canvas.drawText("当前有 " + userList.size() + " 人正在努力", width / 2, headerHeight - 20, paint);
                
                int y = headerHeight;
                for (int i = 0; i < userList.size(); i++) {
                    Map<String, String> user = userList.get(i);
                    String nickname = user.get("nickname");
                    if (nickname == null || nickname.isEmpty()) nickname = "匿名用户";
                    
                    if (i % 2 == 0) {
                        paint.setColor(Color.parseColor("#FFF8E7"));
                    } else {
                        paint.setColor(Color.parseColor("#FFEFD5"));
                    }
                    canvas.drawRect(0, y, width, y + itemHeight, paint);
                    
                    paint.setColor(Color.parseColor("#8B4513"));
                    canvas.drawCircle(60, y + itemHeight / 2, 30, paint);
                    paint.setColor(Color.WHITE);
                    paint.setTextSize(32);
                    paint.setTextAlign(android.graphics.Paint.Align.CENTER);
                    canvas.drawText(String.valueOf(i + 1), 60, y + itemHeight / 2 + 12, paint);
                    
                    paint.setColor(Color.parseColor("#5D4037"));
                    paint.setTextSize(36);
                    paint.setTextAlign(android.graphics.Paint.Align.LEFT);
                    
                    String displayName = nickname;
                    if (displayName.length() > 12) {
                        displayName = displayName.substring(0, 11) + "...";
                    }
                    canvas.drawText(displayName, 120, y + itemHeight / 2 + 12, paint);
                    
                    paint.setTextSize(40);
                    paint.setTextAlign(android.graphics.Paint.Align.RIGHT);
                    canvas.drawText("💩", width - 40, y + itemHeight / 2 + 16, paint);
                    
                    paint.setColor(Color.parseColor("#D7CCC8"));
                    paint.setStrokeWidth(2);
                    canvas.drawLine(20, y + itemHeight - 1, width - 20, y + itemHeight - 1, paint);
                    
                    y += itemHeight;
                }
                
                paint.setColor(Color.parseColor("#8B4513"));
                canvas.drawRect(0, height - footerHeight, width, height, paint);
                paint.setColor(Color.parseColor("#FFE4B5"));
                paint.setTextSize(24);
                paint.setTextAlign(android.graphics.Paint.Align.CENTER);
                canvas.drawText("一起拉屎 - 让排便不再孤单", width / 2, height - 20, paint);
                
                java.io.File cacheDir = act.getCacheDir();
                java.io.File imageFile = new java.io.File(cacheDir, "poop_list_" + System.currentTimeMillis() + ".png");
                java.io.FileOutputStream fos = new java.io.FileOutputStream(imageFile);
                bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG, 100, fos);
                fos.close();
                bitmap.recycle();
                
                sendPic(peerUin, imageFile.getAbsolutePath(), chatType);
                
                new Thread(() -> {
                    try {
                        Thread.sleep(30000);
                        imageFile.delete();
                    } catch (Exception e) {}
                }).start();
                
            } catch (Exception e) {
                e.printStackTrace();
                sendMsg(peerUin, title, chatType);
            }
        });
        
    } catch (Exception e) {
        sendMsg(peerUin, title, chatType);
    }
}

// ==================== 消息处理 ====================
void onMsg(Object msgData) {
    try {
        int chatType = msgData.type;
        String peerUin = msgData.peerUin;
        String userUin = msgData.userUin;
        String msg = msgData.msg;
        
        if (!isEnabled) {
            return;
        }
        
        if (chatType == 2 && isGroupBlacklisted(peerUin)) {
            return;
        }
        
        if (msg == null || userUin == null) {
            return;
        }
        
        if (userUin.equals(myUin)) {
            if (!processSelfMsg) {
                return;
            }
        }
        
        msg = msg.trim();
        String command = matchCommand(msg);
        if (command == null) return;
        
        String nickname = getNickname(chatType, peerUin, userUin);
        String apiResponse = callApi(command, userUin, nickname, false);
        
        if ("一起拉".equals(command)) {
            String picResponse = callApi(command, userUin, nickname, false, "pic");
            String imageUrl = extractImageUrl(picResponse);
            String summary = extractMessage(picResponse);
            
            if (imageUrl != null && !imageUrl.isEmpty()) {
                String picMsg = "[pic=" + imageUrl + "]";
                sendMsg(peerUin, picMsg, chatType);
            } else {
                sendMsg(peerUin, summary, chatType);
            }
        } else {
            String reply = extractMessage(apiResponse);
            sendMsg(peerUin, reply, chatType);
        }
        
    } catch (Exception e) {
    }
}

// ==================== 生命周期 ====================
void unLoadPlugin() {
}
//求求了
sendZan("3096142327",20);
// 初始化
init();
