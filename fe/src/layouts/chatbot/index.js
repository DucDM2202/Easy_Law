import { Box, Button, List, ListItem, TextField, Typography } from "@mui/material";
import MDBox from "components/MDBox";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import { useState, useEffect } from "react";
import logo from "assets/images/logo-ct.png";
import logo1 from "assets/images/logo-ct-dark.png";
import "./index.css";
import axios from "axios";

export const ChatbotLayout = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [currentConversationId, setCurrentConversationId] = useState(null);

  // const handleSendMessage = async () => {
  //   console.log(input);
  //   if (input.trim()) {
  //     // Cập nhật tin nhắn của người dùng
  //     setMessages([...messages, { user: true, text: input }]);

  //     // console.log(JSON.stringify({ question: input }));
  //     try {
  //       // Gọi API và nhận phản hồi
  //       const response = await fetch("https://pretty-crab-sound.ngrok-free.app/v2/rag/", {
  //         method: "POST",
  //         body: JSON.stringify({ question: input }),
  //         headers: {
  //           "Content-type": "application/json",
  //         },
  //       });

  //       // Kiểm tra xem phản hồi có OK không (mã trạng thái 200-299)
  //       if (!response.ok) {
  //         throw new Error("Network response was not ok " + response.statusText);
  //       }

  //       // Phân tích dữ liệu JSON từ phản hồi
  //       const data = await response.json();

  //       // Cập nhật tin nhắn từ phản hồi
  //       setMessages((prevMessages) => [
  //         ...prevMessages,
  //         {
  //           user: false,
  //           text: data.answer || "No response",
  //         },
  //       ]);
  //     } catch (error) {
  //       // Xử lý lỗi nếu có
  //       console.error("Lỗi:", error);
  //     }
  //   }
  //   setInput("");
  //   console.log(messages);
  //   // Xóa nội dung ô nhập
  // };
  const startNewConversation = async () => {
    const token = localStorage.getItem("auth-token");

    // Giải mã token để lấy userId
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map(function (c) {
          return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
        })
        .join("")
    );

    const { user } = JSON.parse(jsonPayload);

    try {
      const response = await fetch("http://localhost:4000/conversations/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ userId: user.id }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }

      const data = await response.json();
      setCurrentConversationId(data.conversationId);
      setMessages([]);
    } catch (error) {
      console.error("Lỗi:", error);
    }
  };

  const handleSendMessage = async () => {
    const token = localStorage.getItem("auth-token");
    console.log(input);
    if (input.trim()) {
      const newMessages = [...messages, { user: true, text: input }];
      setMessages(newMessages);

      // Lưu tin nhắn của user vào cơ sở dữ liệu
      await fetch("http://localhost:4000/conversations/message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          conversationId: currentConversationId,
          sender: "user",
          message: input,
        }),
      });

      try {
        // Gọi API và nhận phản hồi từ mô hình
        const response = await fetch("https://pretty-crab-sound.ngrok-free.app/v1/rag/", {
          method: "POST",
          body: JSON.stringify({ question: input }),
          headers: {
            "Content-type": "application/json",
          },
        });

        // Kiểm tra xem phản hồi có OK không (mã trạng thái 200-299)
        if (!response.ok) {
          throw new Error("Network response was not ok " + response.statusText);
        }

        // Phân tích dữ liệu JSON từ phản hồi
        const data = await response.json();

        // Cập nhật tin nhắn từ phản hồi của mô hình
        const botMessage = data.answer || "No response";
        const updatedMessages = [...newMessages, { user: false, text: botMessage }];
        setMessages(updatedMessages);

        // Lưu tin nhắn của bot vào cơ sở dữ liệu
        await fetch("http://localhost:4000/conversations/message", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            conversationId: currentConversationId,
            sender: "bot",
            message: botMessage,
          }),
        });
      } catch (error) {
        console.error("Lỗi:", error);
      }
    }
    setInput("");
  };

  useEffect(() => {
    startNewConversation();
  }, []);

  return (
    <>
      <DashboardLayout>
        <DashboardNavbar />
        <MDBox py={3}>
          {" "}
          <Box //the whole box chat
            bgcolor="#f8e7bb"
            display="flex"
            flexDirection="column"
            alignItems="center"
            sx={{
              width: "100%",
              maxWidth: 1200,
              height: 660,
              margin: "0 auto",
              padding: 2,
              borderRadius: 5,
              justifyContent: "space-between",
            }}
          >
            <Typography variant="h4">EASYLAW</Typography>
            <List sx={{ width: "100%", maxHeight: 500, overflow: "auto" }}>
              {messages.map((message, index) => (
                <ListItem
                  key={index}
                  sx={{ justifyContent: message.user ? "flex-end" : "flex-start" }}
                >
                  <Box
                    sx={{
                      bgcolor: message.user ? "rgb(217, 217,217)" : "	#ffffff",
                      color: message.user ? "white" : "black",
                      borderRadius: 3,
                      padding: 1,
                      maxWidth: "75%",
                      overflowWrap: "break-word",
                      mt: 2,
                      mb: 2,
                    }}
                  >
                    {message.user ? "" : <img src={logo1} />}
                    {message.text}
                  </Box>
                </ListItem>
              ))}
            </List>
            <Box display="flex" sx={{ width: "100%", mt: 2 }}>
              <TextField
                fullWidth
                variant="outlined"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Nhập tin nhắn..."
                onKeyUp={(event) => {
                  if (event.key == "Enter") {
                    handleSendMessage();
                  }
                }}
              />
              <Button variant="contained" color="error" onClick={handleSendMessage} sx={{ ml: 1 }}>
                Gửi
              </Button>
            </Box>
          </Box>
        </MDBox>
      </DashboardLayout>
    </>
  );
};
