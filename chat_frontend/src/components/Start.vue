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
                                        <button @click="handleClickTwoSteps">
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
                                <div class="flex py-1 h-10 px-2 w-auto gap-1">
                                    <DocumentIcon v-if="file.type === 'application/pdf'"
                                        class="rounded-full h-6 w-6 px-1 bg-red-200 text-white" />
                                    <DocumentIcon v-else class="rounded-full h-6 w-6 px-1 bg-blue-200 text-white" />
                                    <div class="truncate w-full">{{ file.name }}</div>
                                    <XCircleIcon @click="removeFile(index)" class="rounded-full h-8 w-8 px-1 bg-green-200 text-black"/>
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
import { DocumentIcon, XCircleIcon } from "@heroicons/vue/24/outline";
import { useToast } from 'vue-toastification';
import { useRoute } from 'vue-router';
import router from '../router/index.js';
import { getCurrentInstance } from 'vue';
const { proxy } = getCurrentInstance();

const username = localStorage.getItem('username');
const selectedFiles = ref([]);
const conversationTitle = ref('');
const conversationId = ref('');
const userInput = ref('');
const conversation_title = ref('');
const conversation_id = ref('');
const toast = useToast();

const handleClickTwoSteps = async () => {
  await CreateConversation(); // 等待 CreateConversation 完成
  await HandleUploadedFiles(); // 然后再执行 HandleUploadedFiles
};

const removeFile = (index) => {
  selectedFiles.value.splice(index, 1);
};

const toastSuccessMethod = () => {
    toast.info("Upload successfully", {
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
const toastCreateErrorNoMsgMethod = () => {
    toast.error("Ask something first", {
        position: "top-center",
        timeout: 3000,
        closeOnClick: true,
        icon: true,
    });
};
const toastCreateErrorNoFileMethod = () => {
    toast.error("No File Upload", {
        position: "top-center",
        timeout: 3000,
        closeOnClick: true,
        icon: true,
    });
};

const handleFileUpload = (event) => {
  const sFiles = Array.from(event.target.files); // 获取选中的文件
  selectedFiles.value.push(...sFiles); // 将文件添加到 files 数组中，而不是替换
};

const HandleUploadedFiles = () => {
    if (selectedFiles.value.length === 0) {
        toastCreateErrorNoFileMethod();
        return;
    }
    
    if (userInput.value === '') {
        toastCreateErrorNoMsgMethod();
        return;
    }
    
    console.log(selectedFiles.value);
    console.log('Uploaded file:', selectedFiles);
    const username = localStorage.getItem('username');
    const conversationTitle = localStorage.getItem('conversationTitle');
    const conversationId = localStorage.getItem('conversationId');
    console.log("now id??", conversationId)
    console.log(conversationTitle)
    // 使用FormData对象来构建文件上传的请求
    const formData = new FormData();
    //formData.append('file',file)
    selectedFiles.value.forEach(file => {
        formData.append('files', file);
    });
    formData.append('username', username);
    formData.append('conversationTitle', conversationTitle);
    formData.append('conversationId',conversationId);
    console.log(formData);

    axios.post(`${proxy.$apiBaseUrl}/api/upload/`, formData)
        .then(function (response) {
            console.log('Server API upload response:', response);
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
            localStorage.setItem('conversationId', conversation_id.value);
            console.log("idid?:", conversation_id.value);
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

const CreateConversation = async () => {
    if (selectedFiles.value.length === 0) {
        toastCreateErrorNoFileMethod();
        return;
    }
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
        console.log("conversation_id: ", response.data.conversation_id);
        conversation_id.value = response.data.conversation_id;
        localStorage.setItem('conversationId', conversation_id.value);
        console.log("ls:", localStorage.getItem('conversationId'));

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
</script>