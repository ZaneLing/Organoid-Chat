<template>
    <div class="flex flex-col bg-blue-300 h-screen justify-center">
        <div class="flex justify-center h-40 w-auto p-3">
            <img class="rounded-full" src="../assets/OC-logo.jpg" alt="OpenConext Logo">
        </div>

        <div class="flex justify-center h-auto w-auto">
            <div class="flex flex-col bg-white justufy-center h-atuo w-8/12 rounded-lg shadow gap-2">
                <form @submit.prevent="sendMessageandFiles">
                    <!--message input-->
                    <div class="p-2 justify-center rounded-lg text-left bg-white h-40 w-auto">
                        <textarea id="userInput" v-model="userInput" rows="6" placeholder="Ask anything about organoid..."
                            class="block border-none active:border-white active:outline-white outline-white w-full h-full resize-none rounded-md px-3.5 py-2 font-semibold text-blue-900 sm:text-xl sm:leading-6"></textarea>
                    </div>
                    <!--send file-->
                    <div class="flex flex-row-reverse h-8 pb-10">
                        <div>
                            <div class="flex flex-row">
                                <form @submit.prevent="uploadFile" class="flex flex-row gap-4">
                                    <div class="flex h-full">
                                        <label for="file-upload" class="flex">
                                            <PaperClipIcon
                                                class="w-8 h-8 rounded-lg text-blue-900 hover:bg-indigo-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2" />
                                        </label>
                                        <input id="file-upload" type="file" @change="handleFileUpload" multiple
                                            class="hidden" />
                                    </div>
                                    <div class="w-auto h-full items-center justify-center pr-3">
                                        <button @click="async () => {CreateConversation();HandleUploadedFiles();}">
                                            <PaperAirplaneIcon
                                                class="w-8 h-8 rounded-lg text-blue-900 cursor-pointer hover:bg-indigo-100" />
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                    <!--show file-->
                    <div v-if="selectedFiles.length" class="flex">
                        <ul class="list-none flex flex-col pl-2 rouned-full">
                            <li v-for="(file, index) in selectedFiles" :key="index"
                                class="bg-white gap-1 text-blue-400 rounded-3xl">
                                <div class="flex py-2 h-10 px-2 w-auto gap-1">
                                    <DocumentIcon v-if="file.type === 'application/pdf'"
                                        class="rounded-full h-6 w-6 px-1 bg-red-200 text-white" />
                                    <DocumentIcon v-else class="rounded-full h-6 w-6 px-1 bg-blue-200 text-white" />
                                    {{ file.name }}
                                </div>
                            </li>
                        </ul>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

import PaperClipIcon from '@heroicons/vue/24/outline/PaperClipIcon';
import PaperAirplaneIcon from '@heroicons/vue/24/outline/PaperAirplaneIcon';
import { DocumentIcon } from "@heroicons/vue/24/outline";
import { useToast } from 'vue-toastification';
import { useRoute } from 'vue-router';
import router from '../router/index.js';
import { getCurrentInstance } from 'vue';
const { proxy } = getCurrentInstance();

const username = localStorage.getItem('username');
const selectedFiles = ref([]);
const conversationTitle = ref('');
const userInput = ref('');
const conversation_title = ref('');
const toast = useToast();
const toastDeleteMethod = () => {
    toast.info("Delete successfully", {
        position: "top-center",
        timeout: 1500,
        closeOnClick: true,
        icon: true,
    });
};
const toastLoginErrorMethod = () => {
    toast.error("Please login first", {
        position: "top-center",
        timeout: 3000,
        closeOnClick: true,
        icon: true,
    });
};
const toastSuccessMethod = () => {
    toast.info("Upload successfully", {
        position: "top-center",
        timeout: 1500,
        closeOnClick: true,
        icon: true,
    });
};
const toastSuccessUploadMethod = () => {
    toast.info("Upload File successfully", {
        position: "top-center",
        timeout: 1500,
        closeOnClick: true,
        icon: false,
    });
};
const toastOpenErrorMethod = () => {
    toast.error("Open failed", {
        position: "top-center",
        timeout: 1500,
        closeOnClick: true,
        icon: true,
    });
};
const toastCreateMsgMethod = () => {
    toast.success("Msg created!", {
        position: "top-center",
        timeout: 1500,
        closeOnClick: true,
        icon: true,
    });
};
const toastCreateSuccessMethod = () => {
    toast.success("Create Conversation!", {
        position: "top-center",
        timeout: 1500,
        closeOnClick: true,
        icon: true,
    });
};
// Handle file upload


const handleFileUpload = (event) => {
    selectedFiles.value = Array.from(event.target.files);
};

const HandleUploadedFiles = () => {
    //file.value = event.target.files[0];
    console.log(selectedFiles.value);
    console.log('Uploaded file:', selectedFiles);
    const username = localStorage.getItem('username');
    const conversationTitle = localStorage.getItem('conversationTitle');
    // 使用FormData对象来构建文件上传的请求
    const formData = new FormData();
    //formData.append('file',file)
    selectedFiles.value.forEach(file => {
        formData.append('files', file);
    });
    formData.append('username', username);
    formData.append('conversationTitle', conversationTitle);
    console.log(formData);

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
            localStorage.setItem('conversationTitle', conversation_title.value);
            console.log(conversation_title.value);
            router.push(`/base/conversation/${conversation_title.value}`);

            // 清空 selectedFiles
            selectedFiles.value = [];
        }
        )
        .catch(function (error) {
            console.log('Error loading file:', error);
        });
};

const createMessage = async (messageContent, messageRole) => {
    try {
        console.log("---------");
        const conversationTitle = localStorage.getItem('conversationTitle');
        console.log(conversationTitle);
        const response = await axios.post(`${proxy.$apiBaseUrl}/api/createmessage/`, {
            conversation_title: conversationTitle,
            message_role: messageRole,
            message_content: messageContent
        });
        console.log(response);
        toastCreateMsgMethod();
    } catch (error) {
        console.log(error);
    }
};

const CreateConversation = async () => {
    try {
        console.log("start create!!!!")
        let currentMsg = userInput.value;
        conversation_title.value = userInput.value.substring(0, 20);
        localStorage.setItem('conversationTitle', conversation_title.value);
        const response = await axios.post(`${proxy.$apiBaseUrl}/api/createconversation/`, {
            message: userInput.value,
            user: username,
        },
            {
                headers: {
                    'Content-Type': 'application/json',
                }
            }
        );
        console.log(response.data);
        
        if (response.data) {
            console.log("start create msg!!!");
            //createMessage(currentMsg, 'user');
            console.log("Create Success");
            toastCreateSuccessMethod();
        }
    }

    catch (error) {
        console.log(error);
    }
};
const SaveConversationFile = async () => {
    if (selectedFiles.value.length == 0) return;
    try {
        const formData = new FormData();

        console.log(conversation_title.value);
        formData.append('conversation_title', conversation_title.value);
        selectedFiles.value.forEach(file => {
            formData.append('files', file);
        });
        formData.append('username', username);
        console.log(selectedFiles);
        console.log(formData);
        const response = await axios.post(`${proxy.$apiBaseUrl}/api/saveconversationfile/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        console.log(response);
        toastSuccessUploadMethod();
    } catch (error) {
        console.log(error);
    }
};
import { useRouter } from 'vue-router';
</script>