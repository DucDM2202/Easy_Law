const port = 4000;
const jwt = require('jsonwebtoken');
const express = require('express');
const app = express();
const mongoose = require('mongoose');
const cors = require('cors');
const http = require('http');
const socketIo = require('socket.io');
const bcrypt = require('bcryptjs'); // Sử dụng bcrypt để mã hóa mật khẩu

app.use(express.json());
app.use(cors());

// Database connection with mongoDB
mongoose.connect("mongodb+srv://NguyenMinhHuong:02082004@cluster0.rlceca4.mongodb.net/EASYLAW", {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

// API creation
app.get("/", (req, res) => {
    res.send("Express App is running")
});

// Tạo Schema cho mô hình user
const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    birthday: {
        type: Date,
    },
    email: {
        type: String,
        unique: true,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    conversations: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Conversation'
    }]
});

const Users = mongoose.model("Users", userSchema);

// Tạo Schema cho cuộc trò chuyện
const conversationSchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Users',
        required: true
    },
    messages: [{
        sender: {
            type: String, // "user" hoặc "bot"
            required: true
        },
        message: {
            type: String,
            required: true
        },
        timestamp: {
            type: Date,
            default: Date.now
        }
    }],
    startedAt: {
        type: Date,
        default: Date.now
    },
    endedAt: {
        type: Date
    }
});

const Conversation = mongoose.model('Conversation', conversationSchema);

// Function to start a new conversation
async function startConversation(userId) {
    const conversation = new Conversation({
        userId: userId
    });

    await conversation.save();

    await Users.findByIdAndUpdate(userId, {
        $push: { conversations: conversation._id }
    });

    return conversation._id;
}

// Function to save a message in a conversation
async function saveMessage(conversationId, sender, message) {
    await Conversation.findByIdAndUpdate(conversationId, {
        $push: { messages: { sender: sender, message: message } }
    });
}

// Function to get a conversation by ID
async function getConversation(conversationId) {
    const conversation = await Conversation.findById(conversationId).exec();
    return conversation;
}

// Function to get all conversations for a user
async function getUserConversations(userId) {
    // const user = await Users.findById(userId).populate('conversations').exec();
    // return user.conversations;
    // Tìm người dùng và populate cuộc trò chuyện
    const user = await Users.findById(userId).populate({
        path: 'conversations',
        select: 'messages', // Chỉ lấy trường messages
        model: 'Conversation'
    }).exec();

    // Trả về thông tin tin nhắn trong tất cả các cuộc trò chuyện
    const messages = user.conversations.flatMap(conversation => conversation.messages);
    return messages;
}

// Creating Endpoint for registering the user
app.post('/signup', async (req, res) => {
    try {
        let check = await Users.findOne({ email: req.body.email });
        if (check) {
            return res.status(400).json({ success: false, errors: "existing user found with same email address" });
        }

        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(req.body.password, salt);

        const user = new Users({
            name: req.body.username,
            email: req.body.email,
            password: hashedPassword,
            birthday: req.body.birthday
        });

        await user.save();

        const data = {
            user: {
                id: user.id,
            },
        };
        const token = jwt.sign(data, 'secret_ecom');
        res.json({ success: true, token, userId: user.id });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Creating Endpoint for login the user
app.post('/login', async (req, res) => {
    try {
        let user = await Users.findOne({ email: req.body.email });
        if (!user) {
            return res.status(400).json({ success: false, errors: "User not found" });
        }

        const passCompare = await bcrypt.compare(req.body.password, user.password);
        if (!passCompare) {
            return res.status(400).json({ success: false, errors: "Password is incorrect" });
        }

        const data = {
            user: {
                id: user.id,
                name: user.name
            },
        };
        const token = jwt.sign(data, 'secret_ecom');
        res.json({ success: true, token, userId: user.id, name: user.name });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Endpoint để bắt đầu một cuộc trò chuyện mới
app.post('/conversations/start', async (req, res) => {
    const { userId } = req.body;
    const conversationId = await startConversation(userId);
    res.json({ success: true, conversationId });
});

// Endpoint để lưu tin nhắn vào cuộc trò chuyện
app.post('/conversations/message', async (req, res) => {
    const { conversationId, sender, message } = req.body;
    await saveMessage(conversationId, sender, message);
    res.json({ success: true });
});

// Endpoint để lấy một cuộc trò chuyện theo ID
app.get('/conversations/:id', async (req, res) => {
    const conversation = await getConversation(req.params.id);
    res.json({ success: true, conversation });
});

// Endpoint để lấy tất cả các cuộc trò chuyện của một user
app.get('/user/:userId/conversations', async (req, res) => {
    const conversations = await getUserConversations(req.params.userId);
    res.json({ success: true, conversations });
});

// Sử dụng Socket.IO để xử lý chat thời gian thực
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*",
    }
});

io.on("connection", (socket) => {
    console.log("New client connected");

    socket.on("message", async (data) => {
        const { conversationId, sender, message } = data;
        await saveMessage(conversationId, sender, message);
        io.to(conversationId).emit("newMessage", { sender, message });
    });

    socket.on("joinConversation", (conversationId) => {
        socket.join(conversationId);
    });

    socket.on("disconnect", () => {
        console.log("Client disconnected");
    });
});

server.listen(port, (error) => {
    if (!error) {
        console.log("Server is running on port 4000");
    }
    else {
        console.log("Error:" + error);
    }
});
