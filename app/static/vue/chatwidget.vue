<template>
    <div class="chat-window" :style="{backgroundColor: backgroundColor, color: textColor}">
      <div class="chatroom-selection">
        <label for="chatroom">Choose a chatroom:</label>
        <select id="chatroom" v-model="selectedChatroom">
          <option v-for="chatroom in chatrooms" :key="chatroom.id" :value="chatroom.id">{{ chatroom.name }}</option>
        </select>
      </div>
      <div class="messages">
        <p v-for="msg in messages" :key="msg.id">{{ msg.text }}</p>
      </div>
      <div class="input-container">
        <input type="text" v-model="inputMessage" @keyup.enter="sendMessage" placeholder="Type your message here..." />
        <button @click="sendMessage">Send</button>
      </div>
      <button class="hidden-button" @click="hiddenAction">Hidden Button</button>
    </div>
  </template>

<script>
export default {
  data() {
    return {
      chatrooms: [
        { id: 1, name: 'ChatGPT' },
        { id: 2, name: 'Stable Diffusion' },
        { id: 3, name: 'Acrocat Ranch' },
        { id: 3, name: 'Cafe Fred' },
      ],
      selectedChatroom: 1,
      messages: [
        { id: 1, text: 'Hello, welcome to the chat!' },
        { id: 2, text: 'This is a sample message.' },
      ],
      inputMessage: '',
      backgroundColor: '#ffffff',
      textColor: '#000000',
    };
  },
  methods: {
    sendMessage() {
      if (this.inputMessage.trim() !== '') {
        const newMessage = {
          id: this.messages.length + 1,
          text: this.inputMessage,
        };
        this.messages.push(newMessage);
        this.inputMessage = '';
      }
    },
    hiddenAction() {
      // Add your hidden action here
      console.log('Hidden button clicked!');
    },
  },
};
</script>

<style scoped>
.chat-window {
  width: 500px;
  height: 300px;
  padding: 20px;
  border: 1px solid #cccccc;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chatroom-selection {
  display: flex;
  align-items: center;
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
  border: 1px solid #cccccc;
  padding: 10px;
  border-radius: 5px;
}

.input-container {
  display: flex;
  gap: 5px;
}

input[type='text'] {
  flex-grow: 1;
  padding: 5px;
  border: 1px solid #cccccc;
  border-radius: 5px;
}

button {
  padding: 5px 10px;
  border: 1px solid #cccccc;
  background-color: #ffffff;
  color: #000000;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #cccccc;
}

.hidden-button {
  position: absolute;
  top: 0;
  right: 0;
  opacity: 0;
  width: 50px;
  height: 50px;
}

.hidden-button:hover {
  opacity: 0.3;
}

.hidden-button:focus {
  opacity: 0.5;
}
</style>
