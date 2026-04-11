import asyncio
import json
import os
import urllib.parse
from typing import Any, Optional

import aiohttp

from astrbot.api import sp, logger
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

from .quotes import get_random_quote, get_quote_from_api
from .local_data import start_local_poop, end_local_poop, get_local_poop_list


# 常量定义
class Actions:
    START = "拉屎"
    LIST = "一起拉"
    END = "拉完了"


# 错误消息常量
ERROR_API_FAILED = "⚠️ 服务器连接失败，已切换至本地模式！"


def is_valid_url(url: str) -> bool:
    if not url:
        return False
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except (ValueError, TypeError):
        return False


@register("一起拉", "喃喃", "屎壳郎戴面具——臭不要脸！厕所里跳高——过粪了！带薪拉屎组队，马桶上开黑！", "0.5")
class YiQiLaPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)

        self.api_url = config.get("api_url", "https://api-fast.521567.xyz/api/yql/")
        self.api_key = config.get("api_key") or os.getenv("YQL_API_KEY")
        self.base_url = "https://api-fast.521567.xyz"

        if not self.api_key:
            logger.warning("未配置 API Key，请通过配置文件或环境变量 YQL_API_KEY 设置")
            self.api_key = ""

        self.enabled = sp.get("yql_enabled", config.get("enabled", True))
        self.process_self_msg = sp.get("yql_process_self_msg", config.get("process_self_msg", False))
        self.group_blacklist = sp.get("yql_group_blacklist", config.get("group_blacklist", []))

        # 便秘一言开关
        self.enable_quote_on_start = sp.get("yql_quote_on_start", config.get("enable_quote_on_start", True))
        self.enable_quote_on_end = sp.get("yql_quote_on_end", config.get("enable_quote_on_end", True))

        self.session: Optional[aiohttp.ClientSession] = None

        logger.info("一起拉屎插件已加载！")

    async def initialize(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))

    async def terminate(self):
        if self.session:
            await self.session.close()
        logger.info("一起拉屎插件已卸载！")

    def _mask_sensitive_info(self, text: str) -> str:
        """隐藏敏感信息（如 API Key）"""
        if self.api_key and text:
            return text.replace(self.api_key, "***")
        return text

    def _sanitize_input(self, text: str, max_length: int = 100) -> str:
        """清理用户输入"""
        if not text:
            return ""
        # 限制长度
        text = text[:max_length]
        # 移除控制字符
        text = ''.join(char for char in text if ord(char) >= 32)
        return text.strip()

    async def _call_api(self, action: str, qq: str, nickname: str,
                        show_qq: bool = False, format_type: str = "text") -> Optional[str]:
        if not self.session:
            logger.error("HTTP session 未初始化")
            return None

        if not self.api_key:
            logger.error("API Key 未配置")
            return None

        try:
            params = {
                "key": self.api_key,
                "action": action,
                "qq": self._sanitize_input(qq, 20),
                "nickname": self._sanitize_input(nickname, 50)
            }
            if show_qq:
                params["qqtrue"] = "true"
            if format_type != "text":
                params["format"] = format_type

            url = self.api_url + "?" + urllib.parse.urlencode(params)
            safe_url = self._mask_sensitive_info(url)
            logger.debug(f"API请求: {safe_url}")

            async with self.session.get(url) as response:
                response.raise_for_status()
                result = await response.text()
                logger.debug(f"API响应: {result[:200] if len(result) > 200 else result}")
                return result
        except aiohttp.ClientResponseError as e:
            logger.error(f"API响应错误: {e.status} - {e.message}")
            return None
        except aiohttp.ClientError as e:
            logger.error(f"API网络错误: {e}")
            return None
        except asyncio.TimeoutError:
            logger.error("API请求超时")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"API响应JSON解析失败: {e}")
            return None
        except Exception as e:
            logger.exception(f"API调用时发生未预期错误: {e}")
            return None

    def _parse_api_response(self, api_response: Optional[str]) -> dict[str, Any]:
        if api_response is None:
            return {"message": "接口调用失败"}

        try:
            data = json.loads(api_response)
            return data
        except json.JSONDecodeError as e:
            logger.warning(f"JSON解析失败: {e}, 尝试作为纯文本处理")
            return {"message": api_response}

    async def _check_permission(self, event: AstrMessageEvent) -> bool:
        if not self.enabled:
            return False

        group_id = event.get_group_id()
        if group_id and group_id in self.group_blacklist:
            return False

        return True

    def _validate_user_info(self, event: AstrMessageEvent) -> tuple[Optional[str], Optional[str]]:
        """验证并返回用户信息"""
        user_id = event.get_sender_id()
        user_name = event.get_sender_name()

        if not user_id or not user_name:
            logger.warning("无法获取用户信息")
            return None, None

        return user_id, user_name

    @filter.command("拉屎", alias={"拉粑粑", "拉臭臭"})
    async def start_poop(self, event: AstrMessageEvent):
        """开始记录拉屎时间"""
        if not await self._check_permission(event):
            return

        user_id, user_name = self._validate_user_info(event)
        if not user_id or not user_name:
            yield event.plain_result("无法获取用户信息，请重试")
            return

        # 发送便秘一言（如果开启）
        if self.enable_quote_on_start:
            # 优先尝试从API获取，失败则使用本地
            quote = await get_quote_from_api(self.session)
            if quote is None:
                quote = get_random_quote()
            yield event.plain_result(f"💩 便秘一言：{quote}\n")

        # 尝试调用 API，如果失败则使用本地兜底
        if self.api_key and self.session:
            api_response = await self._call_api(Actions.START, user_id, user_name, False)
            if api_response:
                data = self._parse_api_response(api_response)
                reply = data.get("message", str(data))
                yield event.plain_result(reply)
                return
            else:
                # API 调用失败，使用本地兜底
                logger.warning("API 调用失败，切换到本地模式")
                yield event.plain_result(ERROR_API_FAILED)
        
        # 本地兜底模式
        local_reply = start_local_poop(user_id, user_name)
        yield event.plain_result(local_reply)

    @filter.command("一起拉", alias={"查看名单", "谁在拉"})
    async def list_poop(self, event: AstrMessageEvent):
        """查看当前正在拉屎的小伙伴"""
        if not await self._check_permission(event):
            return

        user_id, user_name = self._validate_user_info(event)
        if not user_id or not user_name:
            yield event.plain_result("无法获取用户信息，请重试")
            return

        # 尝试调用 API，如果失败则使用本地兜底
        if self.api_key and self.session:
            # 并行调用两个 API，使用 return_exceptions=True 处理部分失败
            results = await asyncio.gather(
                self._call_api(Actions.LIST, user_id, user_name, False),
                self._call_api(Actions.LIST, user_id, user_name, False, "pic"),
                return_exceptions=True
            )

            # 检查是否有异常
            api_response = None
            pic_response = None
            
            if isinstance(results[0], Exception):
                logger.error(f"API调用失败: {results[0]}")
            elif results[0] is None:
                logger.warning("API 返回空，切换到本地模式")
            else:
                api_response = results[0]
            
            if isinstance(results[1], Exception):
                logger.error(f"图片API调用失败: {results[1]}")
                pic_response = None
            else:
                pic_response = results[1]

            if api_response:
                data = self._parse_api_response(api_response)

                if pic_response:
                    pic_data = self._parse_api_response(pic_response)
                    image_url = pic_data.get("image_url")

                    # 处理相对路径，补全为完整URL
                    if image_url and not image_url.startswith(("http://", "https://")):
                        image_url = urllib.parse.urljoin(self.base_url, image_url)

                    if image_url and is_valid_url(image_url):
                        try:
                            yield event.image_result(image_url)
                            return
                        except aiohttp.ClientError as e:
                            logger.warning(f"网络错误，发送图片失败: {e}, 回退到文本")
                        except Exception as e:
                            logger.warning(f"发送图片失败: {e}, 回退到文本")
                
                # 无图片或图片发送失败，返回文本
                summary = data.get("message", str(data))
                yield event.plain_result(summary)
                return

        # 本地兜底模式
        yield event.plain_result(f"{ERROR_API_FAILED}\n")
        local_reply = get_local_poop_list()
        yield event.plain_result(local_reply)

    @filter.command("拉完了", alias={"拉完", "拉完了啦", "结束拉屎"})
    async def end_poop(self, event: AstrMessageEvent):
        """结束拉屎记录"""
        if not await self._check_permission(event):
            return

        user_id, user_name = self._validate_user_info(event)
        if not user_id or not user_name:
            yield event.plain_result("无法获取用户信息，请重试")
            return

        # 尝试调用 API，如果失败则使用本地兜底
        if self.api_key and self.session:
            api_response = await self._call_api(Actions.END, user_id, user_name, False)
            if api_response:
                data = self._parse_api_response(api_response)
                reply = data.get("message", str(data))
                yield event.plain_result(reply)
            else:
                # API 调用失败，使用本地兜底
                logger.warning("API 调用失败，切换到本地模式")
                yield event.plain_result(ERROR_API_FAILED)
                local_reply = end_local_poop(user_id, user_name)
                yield event.plain_result(local_reply)
        else:
            # 本地兜底模式
            local_reply = end_local_poop(user_id, user_name)
            yield event.plain_result(local_reply)

        # 发送便秘一言（如果开启）
        if self.enable_quote_on_end:
            # 优先尝试从API获取，失败则使用本地
            quote = await get_quote_from_api(self.session)
            if quote is None:
                quote = get_random_quote()
            yield event.plain_result(f"\n💩 今日便秘金句：{quote}")

    @filter.command("便秘一言", alias={"拉屎金句", "厕所文学"})
    async def random_quote_cmd(self, event: AstrMessageEvent):
        """随机获取一条便秘一言"""
        if not await self._check_permission(event):
            return

        # 优先尝试从API获取，失败则使用本地
        quote = await get_quote_from_api(self.session)
        if quote is None:
            quote = get_random_quote()
        yield event.plain_result(f"💩 便秘一言：{quote}")

    @filter.command("开关插件")
    @filter.permission_type(filter.PermissionType.ADMIN)
    async def toggle_plugin(self, event: AstrMessageEvent):
        """启用/禁用插件功能"""
        self.enabled = not self.enabled
        sp.put("yql_enabled", self.enabled)
        msg = f"一起拉屎插件已{'启用' if self.enabled else '禁用'}"
        yield event.plain_result(msg)

    @filter.command("处理自己消息")
    @filter.permission_type(filter.PermissionType.ADMIN)
    async def toggle_process_self_msg(self, event: AstrMessageEvent):
        """是否响应自己发送的指令"""
        self.process_self_msg = not self.process_self_msg
        sp.put("yql_process_self_msg", self.process_self_msg)
        msg = f"处理自己消息已{'开启' if self.process_self_msg else '关闭'}"
        yield event.plain_result(msg)

    @filter.command("群黑名单")
    @filter.permission_type(filter.PermissionType.ADMIN)
    async def manage_blacklist(self, event: AstrMessageEvent):
        """管理不响应插件的群聊"""
        group_id = event.get_group_id()

        if not group_id:
            yield event.plain_result("仅在群聊中可用")
            return

        if group_id in self.group_blacklist:
            self.group_blacklist.remove(group_id)
            sp.put("yql_group_blacklist", self.group_blacklist)
            yield event.plain_result("已从黑名单移除当前群")
        else:
            self.group_blacklist.append(group_id)
            sp.put("yql_group_blacklist", self.group_blacklist)
            yield event.plain_result("已添加当前群到黑名单")

    @filter.command("开关便秘一言")
    @filter.permission_type(filter.PermissionType.ADMIN)
    async def toggle_quote(self, event: AstrMessageEvent):
        """开关便秘一言功能"""
        self.enable_quote_on_start = not self.enable_quote_on_start
        self.enable_quote_on_end = self.enable_quote_on_start
        sp.put("yql_quote_on_start", self.enable_quote_on_start)
        sp.put("yql_quote_on_end", self.enable_quote_on_end)
        status = "开启" if self.enable_quote_on_start else "关闭"
        yield event.plain_result(f"便秘一言已{status}（开始和结束时都会触发）")

    @filter.command("测试连接")
    @filter.permission_type(filter.PermissionType.ADMIN)
    async def test_connection(self, event: AstrMessageEvent):
        """测试API服务器连接状态"""
        if not self.session:
            yield event.plain_result("HTTP session 未初始化")
            return

        if not self.api_key:
            yield event.plain_result("API Key 未配置，请通过配置文件或环境变量设置")
            return

        try:
            test_url = self.api_url + "?" + urllib.parse.urlencode({
                "key": self.api_key,
                "action": Actions.LIST,
                "qq": "12345",
                "nickname": "测试用户"
            })

            status_code = 0
            async with self.session.get(test_url) as response:
                response.raise_for_status()
                status_code = response.status
                result = await response.text()

            msg = f"API测试成功！\n码: {status_code}\n内容: {result[:100] if len(result) > 100 else result}"
            yield event.plain_result(msg)
        except aiohttp.ClientError:
            logger.error("API测试失败: 网络连接错误")
            yield event.plain_result("API测试失败: 无法连接到服务器，请检查网络")
        except Exception as e:
            logger.error(f"API测试失败: {e}")
            yield event.plain_result("API测试失败，请查看日志了解详情")
