<template>
    <div class="flex h-screen flex-col bg-blue-100">
        <div class="flex h-16 p-4 bg-blue-800 text-white items-center justify-center">
            <h1 class="text-2xl font-semibold">{{ conversationTitle }}</h1>
        </div>

        <div v-if="conversationFiles.length" class="flex h-20 p-4 bg-blue-300 w-full overflow-x-autos">
            <div class="flex w-full overflow-x-auto">
            <ul class="list-none flex flex-row pl-2 rouned-full gap-2 overflow-hidden whitespace-nowrap">
                <li v-for="(file, index) in conversationFiles" :key="index"
                    class="w-36 bg-white text-blue-400 rounded-3xl overflow-hidden">
                    <button class="flex justify-center items-center content-center h-10 pt-1 px-2 w-32 gap-1"
                        @click="openFile(file.id, file.file_format)">
                        <DocumentIcon v-if="file.file_format === 'pdf'"
                            class="rounded-full h-6 w-6 px-1 bg-red-200 text-white" />
                        <DocumentIcon v-else class="rounded-full h-6 w-6 px-1 bg-blue-200 text-white" />
                        <div class="flex h-auto w-24 whitespace-nowrap overflow-hidden">{{ file.filename }}</div>
                    </button>
                </li>
            </ul>
            </div>
        </div>

        <div class="flex-1 p-8 overflow-y-auto" ref="chatContainer">
            <div v-for="(message, index) in messages" :key="index"
                :class="['flex gap-2', message.message_role == 'user' ? 'flex-row-reverse' : 'flex-row']">
                <UserIcon v-if="message.message_role == 'user'" class="h-10 w-10 rounded-full text-white bg-blue-300" />
                <CubeIcon v-else class="h-10 w-10 rounded-full text-white bg-blue-700" />
                <div>
                    <span
                        :class="[message.message_role == 'user' ? 'bg-blue-300' : 'bg-blue-700 text-white', 'inline-block p-3 rounded-lg max-w-xs']">
                        {{ message.message_content }}
                    </span>
                </div>
            </div>
        </div>

        <div v-if="selectedFiles.length" class="flex">
            <ul class="list-none flex gap-2 pl-2 rouned-full">
                <li v-for="(file, index) in selectedFiles" :key="index" class="bg-white gap-1 text-blue-400 rounded-3xl">
                    <div class="flex flex-row py-2 h-10 px-2 gap-2">
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
                            Select and Add File
                        </label>
                        <input id="file-upload" type="file" @change="handleFileUpload" multiple class="hidden" />
                    </div>

                </form>
            </div>
            <div class="flex flex-auto w-full h-full rounded-full bg-white">
                <label for="search-field" class="sr-only">Search</label>
                <div class="flex flex-row relative w-full h-full">
                    <div class="flex w-full">
                        <form class="flex flex-1 py-1.5 w-full h-full" @submit.prevent="sendMessageToLLM">
                            <textarea id="search-field" v-model="userInput" @keydown="handleKeyDown"
                                class="block h-full w-full border-0 bg-transparent items-center justify-center pl-6 pr-0 text-black focus:ring-0 sm:text-sm resize-none focus:border-0 focus:outline-none"
                                placeholder="Send Message to Organoid Chat" type="search" name="search">
                                </textarea>
                            <button type="submit" @click="UploadMessgaeToConversation('user')" class="pr-2">
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
import { XCircleIcon, BookOpenIcon } from "@heroicons/vue/24/outline";
const { proxy } = getCurrentInstance();  // 获取实例代理
const route = useRoute();// 获取动态 conversation_id
const conversationTitle = ref(route.params.conversation_title);
const chatContainer = ref(null);
const scrollToBottom = () => {
    if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
};

const openFile = async (fileId, fileFormat) => {
    try {
        if (fileFormat.toLowerCase() !== 'pdf') {
            toastOpenErrorMethod();
            return; // 直接返回，不继续执行删除操作
        }

        const url = `${proxy.$apiBaseUrl}/api/openfile/${fileId}/`;
        toastOpenSuccessMethod();
        setTimeout(() => {
            window.open(url, '_blank');
        }, 1000);
    } catch (error) {
        console.log(error);
        console.error('Error opening file:', error);
        toastOpenErrorMethod();
    }
};

onMounted(() => {
    console.log(messages);
});

import { UserIcon, CubeIcon } from '@heroicons/vue/24/outline';

const conversationFiles = ref([]);
const messages = ref([]);
const userInput = ref('');

const llamaAPI = new LlamaAI(apiKey);
const apiKey = 'LL-NBo6wEHZ0cx9fReKMf5TL8l8UtH9WDcm5reZXDdYECpIe81oIMhTUSoefbxUbBW1';
//const conversationTitle = localStorage.getItem('conversationTitle');

const sendMessageToLLM = () => {
    console.log("home touch this");
    console.log(userInput.value);
    if (userInput.value.trim().length === 0) {
        return;
    }

    let currentChatMsg = userInput.value.trim().replace(/\n/g, "");

    messages.value.push({
        message_content: userInput.value,
        message_role: 'user'
    });
    userInput.value = '';
    console.log("input not home create")
    createMessage(currentChatMsg, 'user');
    console.log(currentChatMsg);
    scrollToBottom();

    const username = localStorage.getItem('username');
    const conversationTitle = localStorage.getItem('conversationTitle');

    const formData = new FormData();
    formData.append('question', currentChatMsg);
    formData.append('username', username);
    formData.append('conversationTitle', conversationTitle);
    // Send the POST request to the backend
    axios.post('http://172.16.120.14:8091/generate', formData)
        .then((response) => {
            console.log("Response from server:", response.data);
            // Extract the nested response object
            const responseData = response.data;

            const responseDataString = JSON.stringify(response.data);

            // 使用正则表达式提取 answer 字段之后的内容
            const answerMatch = responseDataString.match(/"answer":\s*"(.*?)"/);

            // 如果匹配到，提取答案
            let extractedAnswer = "";
            if (answerMatch && answerMatch[1]) {
                extractedAnswer = answerMatch[1];
            }

            // 输出提取到的 answer 内容
            console.log("Extracted answer:", extractedAnswer);

            messages.value.push({
                message_content: extractedAnswer,
                message_role: 'ai'
            });

            createMessage(extractedAnswer, 'ai');
            scrollToBottom();


            if (responseData && responseData.answer && Array.isArray(responseData.context)) {
                const answer = responseData.answer;
                const uniqueSources = new Set(responseData.context.map(doc => {
                    const parts = doc.metadata.source.split('/');
                    return parts[parts.length - 1];
                }));

                const sources = Array.from(uniqueSources);
                const content = `Answer:\n ${answer}\n\n---------------------------------------------------------\n\nSource:\n${sources.join('\n')}`;
                console.log("Answer:", answer);

            } else {
                console.error("Invalid response format:", response.data);

            }
        })
        .catch((error) => {
            console.error("Error sending message:", error);
            // Handle error
        });
};

const loadConversationMessages = async () => {
    try {
        const response = await axios.post(`${proxy.$apiBaseUrl}/api/getconversationmessages/`, {
            conversationId: localStorage.getItem('conversationId'),
            username: localStorage.getItem('username')
        });
        console.log(response.data);
        messages.value = response.data;

        console.log(messages.value); // 加载并显示消息
    } catch (error) {
        console.error('Failed to load conversation messages:', error);
    }
};

const createMessage = async (messageContent, messageRole) => {
    try {
        const response = await axios.post(`${proxy.$apiBaseUrl}/api/createmessage/`, {
            conversationId: localStorage.getItem('conversationId'),
            message_role: messageRole,
            message_content: messageContent
        });
        scrollToBottom();
    } catch (error) {
        console.error('Failed to create message:', error);
    }
};

onMounted(async () => {
    await loadConversationMessages();
    console.log(messages.value.length);
    if (messages.value.length === 1) {
        console.log('first message!!!');
        responseFirstMessage();
    }
    scrollToBottom();
});

const responseFirstMessage = async () => {
    let userMessage = '';
    userMessage = messages.value[0].message_content;

    let currentChatMsg = userMessage.trim().replace(/\n/g, "");

    scrollToBottom();
    console.log("currentChatMsg: ", currentChatMsg);

    const username = localStorage.getItem('username');
    const conversationTitle = localStorage.getItem('conversationTitle');

    const formData = new FormData();
    formData.append('question', currentChatMsg);
    formData.append('username', username);
    formData.append('conversationTitle', conversationTitle);

    axios.post(`http://172.16.120.14:8091/generate`, formData)
        .then((response) => {
            console.log("start!!!");
            console.log("Response from server:", response.data);
            // Extract the nested response object
            const responseData = response.data;
            
            const responseDataString = JSON.stringify(response.data);

            // 使用正则表达式提取 answer 字段之后的内容
            const answerMatch = responseDataString.match(/"answer":\s*"(.*?)"/);

            // 如果匹配到，提取答案
            let extractedAnswer = "";
            if (answerMatch && answerMatch[1]) {
                extractedAnswer = answerMatch[1];
            }

            // 输出提取到的 answer 内容
            console.log("Extracted answer:", extractedAnswer);

            messages.value.push({
                message_content: extractedAnswer,
                message_role: 'ai'
            });

            createMessage(extractedAnswer, 'ai');
            scrollToBottom();


            if (responseData && responseData.answer && Array.isArray(responseData.context)) {
                const answer = responseData.answer;
                const uniqueSources = new Set(responseData.context.map(doc => {
                    const parts = doc.metadata.source.split('/');
                    return parts[parts.length - 1];
                }));

                const sources = Array.from(uniqueSources);
                const content = `Answer:\n ${answer}\n\n---------------------------------------------------------\n\nSource:\n${sources.join('\n')}`;
            } else {
                console.error("cant get answer:", response.data);
            }
        })
        .catch((error) => {
            console.error("Error sending message:", error);
            // Handle error
        });

};

const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        // 按下 Enter 键时提交表单
        event.preventDefault(); // 阻止默认换行行为
        sendMessageToLLM();
    }
};

const selectedFiles = ref([]);

// 处理文件选择，将文件发给llm之后保存向量数据库
const handleFileUpload = (event) => {
    //file.value = event.target.files[0];
    
    selectedFiles.value = Array.from(event.target.files);
    console.log('Uploaded file:', selectedFiles);
    const username = localStorage.getItem('username');
    const conversationTitle = localStorage.getItem('conversationTitle');
    const conversationId = localStorage.getItem('conversationId');
    console.log('username:', username);
    console.log('conversationTitle:', conversationTitle);
    console.log('conversationId:', conversationId);

    // 使用FormData对象来构建文件上传的请求
    const formData = new FormData();
    //formData.append('file',file)
    selectedFiles.value.forEach(file => {
        formData.append('files', file);
    });
    formData.append('username', username);
    formData.append('conversationTitle', conversationTitle);
    formData.append('conversationId', conversationId);

    axios.post(`${proxy.$apiBaseUrl}/api/upload/`, formData)
        .then(function (response) {
            console.log('Server response:', response);
            toastSuccessMethod();
        }
        )
        .catch(function (error) {
            console.log('Error loading file:', error);
        });
    // 发送FormData对象文件到后端的/Upload路径
    axios.post('http://172.16.120.14:8091/upload', formData)
        .then(function (response) {
            console.log('Server response:', response);
            alert(response.data.response);
            getConversationFiles();
        
        // 清空 selectedFiles
            selectedFiles.value = [];
        }
        )
        .catch(function (error) {
            console.log('Error loading file:', error);
        });
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
const toastOpenSuccessMethod = () => {
    toast.info("Open successfully", {
        position: "top-right",
        timeout: 1000,
        closeOnClick: true,
        icon: true,
    });
};
const toastOpenErrorMethod = () => {
    toast.error("Open Failed", {
        position: "top-right",
        timeout: 3000,
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
        const formData = new FormData();
        console.log(selectedFiles.value);
        formData.append('username', username);
        selectedFiles.value.forEach(file => {
            formData.append('files', file);
        });
        console.log(formData);

        const response = await axios.post(`${proxy.$apiBaseUrl}/api/upload/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        toastSuccessMethod();
    } catch (error) {
        console.log(error);
        toastErrorMethod();
    }
};

const UploadMessgaeToConversation = (messageRole) => {
    console.log(userInput.value)
    try {
        const response = axios.post(`${proxy.$apiBaseUrl}/api/createmessage`, {
            conversationId: localStorage.getItem('conversationId'),
            message_content: userInput.value,
            message_role: messageRole,
        });
        console.log(response.data);
    } catch (error) {
        console.log(error);
    }
};

onMounted(() => {
    getConversationFiles();
    console.log(conversationFiles);
});

const getConversationFiles = async () => {
    try {
        const conversationId = localStorage.getItem('conversationId');
        console.log("id:", conversationId)
        console.log("title:", conversationTitle)
        const response = await axios.post(`${proxy.$apiBaseUrl}/api/getconversationfile/`, {
            username: localStorage.getItem('username'),
            conversationId: localStorage.getItem('conversationId')
        }, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        console.log(response.data);
        conversationFiles.value = response.data.files;
        console.log("files:",conversationFiles);
    } catch (error) {
        console.log(error);
    }
};

</script>