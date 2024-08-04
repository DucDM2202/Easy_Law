import { useState, useEffect } from "react";
import axios from "axios";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import MDBox from "components/MDBox";
import { Box, Button, List, ListItem, TextField, Typography } from "@mui/material";
import logo1 from "assets/images/logo-ct-dark.png";

const History = () => {
  const [conversations, setConversations] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchConversations = async () => {
      try {
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
        console.log("User-----------", user);

        const id = user.id;

        // Lấy danh sách các cuộc trò chuyện
        const response = await axios.get(`http://localhost:4000/user/${id}/conversations`);

        //console.log("response", response.data.conversations[0].messages[0].message);
        console.log("response", response.data.conversations);
        if (response.status === 200) {
          setConversations(response.data.conversations);
        } else {
          throw new Error("Network response was not ok");
        }
      } catch (error) {
        console.error("Error fetching conversations:", error);
        setError(error.message);
      }
    };

    fetchConversations();
  }, []);
  return (
    <DashboardLayout>
      <MDBox
        bgcolor="#f8e7bb"
        py={3}
        display="flex"
        flexDirection="column"
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
        <Typography variant="h4" gutterBottom>
          Lịch sử chatbot
        </Typography>
        {error && <p>Error: {error}</p>}
        <List sx={{ width: "100%", maxHeight: 500, overflow: "auto" }}>
          {conversations.map((conversation, index) => (
            <ListItem
              key={index}
              sx={{ justifyContent: conversation.sender === "bot" ? "flex-start" : "flex-end" }}
            >
              <Box
                sx={{
                  bgcolor: conversation.sender === "bot" ? "#ffffff" : "rgb(217, 217, 217)",
                  color: "black",
                  borderRadius: 3,
                  padding: 1,
                  maxWidthN: "75%",
                  overflowWrap: "break-word",
                  mt: 2,
                  mb: 2,
                }}
              >
                {conversation.sender != "bot" ? "" : <img src={logo1} />}
                {conversation.message}
              </Box>
            </ListItem>
          ))}
        </List>
      </MDBox>
    </DashboardLayout>
  );

  //   return (
  //     <DashboardLayout>
  //       <MDBox py={3} display="flex" flexDirection="column">
  //         <h1>Lịch sử chatbot</h1>
  //         {error && <p>Error: {error}</p>}
  //         <ListItem key={conversations}>
  //           {conversations.map(
  //             (conversation) =>
  //               conversation.sender == "bot" ? (
  //                 <Box
  //                   key={conversation}
  //                   sx={{
  //                     bgcolor: "	#ffffff",
  //                     color: "black",
  //                     borderRadius: 3,
  //                     padding: 1,
  //                     maxWidth: "75%",
  //                     overflowWrap: "break-word",
  //                     mt: 2,
  //                     mb: 2,
  //                     justifyContent: "flex-start",
  //                   }}
  //                 >
  //                   {conversation.message}
  //                 </Box>
  //               ) : (
  //                 <Box
  //                   key={conversation}
  //                   sx={{
  //                     bgcolor: "	#ffffff",
  //                     color: "black",
  //                     borderRadius: 3,
  //                     padding: 1,
  //                     maxWidth: "75%",
  //                     overflowWrap: "break-word",
  //                     mt: 2,
  //                     mb: 2,
  //                     justifyContent: "flex-end",
  //                   }}
  //                 >
  //                   {conversation.message}
  //                 </Box>
  //               )
  //             //<li key={conversation.message}>{conversation.message}</li>
  //           )}
  //         </ListItem>
  //       </MDBox>
  //     </DashboardLayout>
  //   );
};

export default History;
