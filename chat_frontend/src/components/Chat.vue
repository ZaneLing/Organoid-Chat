<template>
    <div class="flex h-screen flex-col bg-blue-100">
        <div class="flex h-16 p-4 bg-blue-800 text-white items-center justify-center">
            <h1 class="text-xl font-semibold">Organoid Chat</h1>
        </div>

        <div class="flex-1 p-8 overflow-y-auto" ref="chatContainer">
            <div v-for="(message, index) in messages" :key="index"
                :class="['flex gap-2', message.isUser ? 'flex-row-reverse' : 'flex-row']">
                <UserIcon v-if="message.isUser" class="h-10 w-10 rounded-full text-white bg-blue-300" />
                <CubeIcon v-else class="h-10 w-10 rounded-full text-white bg-blue-700" />
                <div>
                    <span
                        :class="[message.isUser ? 'bg-blue-300' : 'bg-blue-700 text-white', 'inline-block p-3 rounded-lg max-w-xs']">
                        {{ message.text }}
                    </span>
                </div>
            </div>
        </div>

        <div v-if="selectedFiles.length" class="flex">
            <ul class="list-none flex gap-2 pl-2 rouned-full">
                <li v-for="(file, index) in selectedFiles" :key="index" class="bg-white gap-1 text-blue-400 rounded-3xl">
                    <div class="flex py-2 h-10 px-2 w-auto gap-1">
                        <DocumentIcon v-if="file.type === 'application/pdf'"
                            class="rounded-full h-6 w-6 px-1 bg-red-200 text-white" />
                        <DocumentIcon v-else class="rounded-full h-6 w-6 px-1 bg-blue-200 text-white" />
                        {{ file.name }}
                    </div>
                </li>

            </ul>
        </div>

        <div class="flex h-20 p-4 bg-blue-300 flex-row gap-3">
            <div class="flex flex-row">
                <form @submit.prevent="uploadFile" class="flex flex-row py-1 gap-4">
                    <div class="w-40 h-full items-center">
                        <label for="file-upload"
                            class="block rounded-md items-center justify-center bg-indigo-600 px-3 py-2 text-center text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                            Select File
                        </label>
                        <input id="file-upload" type="file" @change="handleFileUpload" multiple class="hidden" />
                    </div>
                    <div class="w-auto h-full items-center justify-center">
                        <button type="submit"
                            class="block rounded-md items-center justify-center bg-indigo-600 px-3 py-2 text-center text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                            Upload</button>
                    </div>
                </form>
            </div>
            <div class="flex flex-auto w-full h-full rounded-full bg-white">
                <label for="search-field" class="sr-only">Search</label>
                <div class="flex flex-row relative w-full h-full">
                    <div class="flex w-full">
                        <form class="flex flex-1 py-1.5 w-full h-full" @submit.prevent="sendMessage">
                            <textarea id="search-field" v-model="userInput" @keydown="handleKeyDown"
                                class="block h-full w-full border-0 bg-transparent items-center justify-center pl-6 pr-0 text-black focus:ring-0 sm:text-sm resize-none focus:border-0 focus:outline-none"
                                placeholder="Send Message to Organoid Chat" type="search" name="search">
                                </textarea>
                            <button type="submit" class="pr-2">
                                <PaperAirplaneIcon class="bg-blue-300 w-8 h-8 rounded-full text-gray-500 cursor-pointer"
                                    aria-hidden="true" />
                            </button>
                        </form>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import LlamaAI from 'llamaai';
import PaperClipIcon from '@heroicons/vue/24/outline/PaperClipIcon';
import PaperAirplaneIcon from '@heroicons/vue/24/outline/PaperAirplaneIcon';
import { DocumentIcon } from "@heroicons/vue/24/outline";
import { useToast } from 'vue-toastification';
import { marked } from 'marked';
import { useRoute } from 'vue-router';
import { getCurrentInstance } from 'vue';
const { proxy } = getCurrentInstance();  // 获取实例代理

const route = useRoute();

const chatContainer = ref(null);
const scrollToBottom = () => {
    if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
};
const renderMD = (text) => {
    return marked(text);
};

import {
    UserIcon,
    CubeIcon,
} from '@heroicons/vue/24/outline';

const messages = ref([]);
const userInput = ref('');

const llamaAPI = new LlamaAI(apiKey);
const apiKey = 'LL-NBo6wEHZ0cx9fReKMf5TL8l8UtH9WDcm5reZXDdYECpIe81oIMhTUSoefbxUbBW1';

const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        // 按下 Enter 键时提交表单
        event.preventDefault(); // 阻止默认换行行为
        sendMessage();
    }
};

const homeInput = ref('');
onMounted(() => {
    const homeMessage = route.query.homeMessage;
    if (homeMessage) {
        homeInput.value = homeMessage;
    }

});


const sendMessage = async () => {
    if (userInput.value.trim() === '') return;

    console.log(homeInput);
    let userMessage ='';

    if (homeInput.value !== '') {
        messages.value.push({
            text: homeInput.value,
            isUser: true
        });
        userMessage.value = homeInput.value;
        homeInput.value = '';
    }
    else {
        messages.value.push({
            text: userInput.value,
            isUser: true
        });
        userMessage = userInput.value;
        userInput.value = '';
    }
    const apiRequestJson = {
        messages: [{ role: 'user', content: userMessage }],
        stream: false,
        max_tokens: 1000
    };

    try {
        const response = await llamaAPI.run(apiRequestJson);

        const llamaResponse = response.choices[0].message.content;
        console.log(response);
        messages.value.push({
            text: llamaResponse,
            isUser: false
        });
        scrollToBottom();
    } catch (error) {
        console.error('Error during OpenAI API request:', error);
        messages.value.push({
            text: 'Sorry, there was an error with the API request.',
            isUser: false
        });
    }
    scrollToBottom();
};



import { useRouter } from 'vue-router';

const router = useRouter();
//const file = ref(null);
const selectedFiles = ref([]);

// 处理文件选择
const handleFileUpload = (event) => {
    //file.value = event.target.files[0];
    selectedFiles.value = Array.from(event.target.files);
};

const toast = useToast();
const toastSuccessMethod = () => {
    toast.info("Upload successfully", {
    position: "top-right",
    timeout: 1500,
    closeOnClick: true,
    icon: true,
});
};

const toastErrorMethod = () => {
    toast.error("Upload failed", {
    position: "top-right",
    timeout: 4000,
    closeOnClick: true,
    icon: true,
});
};

// Upload file to the backend and save the file name in the db
const uploadFile = async () => {
    try {
        const username = localStorage.getItem('username');
        const authToken = localStorage.getItem('authToken');
        const formData = new FormData();

        console.log(selectedFiles.value);

        formData.append('username', username);

        selectedFiles.value.forEach(file => {
            formData.append('files', file);
        });

        console.log(formData);
        
        
        const response = await axios.post(`${proxy.$apiBaseUrl}/api/upload/`, formData, {
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'multipart/form-data',
            },
        });
        toastSuccessMethod();
    } catch (error) {
        console.log(error);
        toastErrorMethod();
    }
};

</script>