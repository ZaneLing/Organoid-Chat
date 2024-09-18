<template>
    <div class="px-4 sm:px-6 lg:px-8 bg-blue-300 h-screen">
      <div class="sm:flex sm:items-center h-20">
        <div class="sm:flex-auto py-10 h-20">
          <h1 class="font-semibold leading-10 text-3xl text-blue-900">History Chat List of {{ username }}</h1>
        </div>
        <div class="flex flex-col mt-2 sm:ml-16 sm:mt-0 sm:flex-none pt-6 gap-2">
          <button @click="ToSign" type="button"
            class="block rounded-md items-center justify-center bg-indigo-600 px-3 py-1 text-center text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Change
            User</button>
        </div>
      </div>
      <div class="mt-8 flow-root">
        <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <table class="min-w-full table-fixed divide-y text-center divide-gray-300 bg-blue-400">
              <thead class="text-blue-900 text-2xl">
                <tr>
                  <th>Chat id</th>
                  <th>Chat title</th>
                  <th>Open</th>
                  <th>Delete</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="conversation in userConversations" :key="conversation.id" class="text-center text-gray-200 gap-5 h-10">
                  <td>{{ conversation.id }}</td>
                  <td>{{ conversation.title }}</td>
                  <td class="pl-16">
                    <BookOpenIcon class="flex h-6 w-6 rounded-full bg-green-800 text-white" @click="openConversation(conversation.title)" />
                  </td>
                  <td class="pl-16">
                    <XCircleIcon class="flex h-6 w-6 rounded-full bg-red-800 text-white" @click="DeleteConversation(conversation.title)"/>
                  </td>
                </tr>
              </tbody>
            </table>
  
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import router from '../router/index.js';
  import { XCircleIcon, BookOpenIcon } from "@heroicons/vue/24/outline";
  import { useToast } from 'vue-toastification';
  import { getCurrentInstance } from 'vue';
const { proxy } = getCurrentInstance();  // 获取实例代理
  
  const username = localStorage.getItem('username');
  
  const userFiles = ref([]);
  const userConversations = ref([]); 
  const fetchUserConversations = async () => {
    try {
      const response = await axios.post(`${proxy.$apiBaseUrl}/api/getuserconversations/`, {
        user: username
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      userConversations.value = response.data.conversations;
    } catch (error) {
      console.error('Failed to fetch user files:', error);
      toastLoginErrorMethod();
    };
  }
  
  onMounted(() => {
    fetchUserConversations();
  });

  const DeleteConversation = async (conversationTitle) => {
    console.log('delete conversation title:');
    console.log(conversationTitle);
    try {
      const response = await axios.post(`${proxy.$apiBaseUrl}/api/deleteconversation/`, {
        conversation_title: conversationTitle,
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      toastDeleteSuccessMethod();
      fetchUserConversations();
      console.log(response.data);
    } catch (error) {
      console.error('Error deleting file:', error);
      toastDeleteErrorMethod();
    }
  };
  
const openConversation = (conversationTitle) => {
  localStorage.setItem('conversationTitle', conversationTitle);
    router.push(`/base/conversation/${conversationTitle}`); 
};
  
  const fileInput = ref(null);
  
  
  const toast = useToast();
  const toastDeleteSuccessMethod = () => {
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
  const toastOpenMethod = () => {
      toast.info("Open successfully", {
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
  
  const toastDeleteErrorMethod = () => {
      toast.error("Delete failed", {
      position: "top-center",
      timeout: 1500,
      closeOnClick: true,
      icon: true,
  });
  };
  
  // Trigger file input click
  const triggerFileInput = () => {
    fileInput.value.click();
  };
  
  // Handle file upload
  const handleFileUpload = async (event) => {
    const files = event.target.files;
    
    if (files.length === 0) {
      toastErrorMethod();
      return;
    }
  
    // Create a FormData object
    const formData = new FormData();
    
    // Append files to FormData
    Array.from(files).forEach(file => {
      formData.append('files', file);
    });
  
    formData.append('username', username);
  
    try {
      // Send files to the server
      const response = await axios.post(`${proxy.$apiBaseUrl}/api/upload/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });
  
      console.log('Files uploaded successfully:', response.data);
      toastSuccessMethod();
      fetchUserFiles();
      // Handle success (e.g., show a success message or refresh the file list)
    } catch (error) {
      console.error('Error uploading files:', error);
      toastErroMethod();
    }
  };
  
  
  const ToSign = () => {
    router.push('/api/login');
  };

  </script>