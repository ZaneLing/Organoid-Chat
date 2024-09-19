<template>
  <div class="px-4 sm:px-6 lg:px-8 bg-blue-300 h-screen">
    <div class="sm:flex sm:items-center h-20">
      <div class="sm:flex-auto py-10 h-20">
        <h1 class="font-semibold leading-10 text-3xl text-blue-900">File space of {{ username }}</h1>
      </div>
      <div class="flex flex-col mt-2 sm:ml-16 sm:mt-0 sm:flex-none pt-6 gap-2">
        <button @click="ToSign" type="button"
          class="block rounded-md items-center justify-center bg-indigo-600 px-3 py-1 text-center text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Change
          User</button>
        <!-- <button @click="triggerFileInput"
          class="block rounded-md items-center justify-center bg-indigo-600 px-3 py-1 text-center text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
          Add File</button> -->
        <input ref="fileInput" type="file" multiple @change="handleFileUpload" class="hidden" />
      </div>
    </div>
    <div class="mt-8 flow-root">
      <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <table class="min-w-full table-fixed divide-y text-center divide-gray-300 bg-blue-400">
            <thead class="text-blue-900 text-2xl">
              <tr>
                <th>File Name</th>
                <th>Within Conversation</th>
                <th>File Type</th>
                <th>File Size</th>
                <th>Open</th>
                <th>Delete</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="file in userFiles" :key="file.id" class="text-center text-gray-200 gap-5 h-10">
                <td>{{ file.filename }}</td>
                <td>{{ file.file_conversation }}</td>
                <td>{{ file.file_format }}</td>
                <td>{{ (file.file_size / 1024).toFixed(2) }} KB</td>
                <td class="pl-16">
                  <BookOpenIcon class="flex h-6 w-6 rounded-full bg-green-800 text-white" @click="openFile(file.id, file.file_format)" />
                </td>
                <td class="pl-16">
                  <XCircleIcon class="flex h-6 w-6 rounded-full bg-red-800 text-white" @click="deleteFile(file.id)" />
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
import { useRouter } from 'vue-router';


const userFiles = ref([]);

const fetchUserFiles = async () => {
  try {
    const response = await axios.post(`${proxy.$apiBaseUrl}/api/filespace/`, {
      user: username
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    console.log(response.data.files);
    userFiles.value = response.data.files;
  } catch (error) {
    console.error('Failed to fetch user files:', error);
    toastLoginErrorMethod();
    setTimeout(() => {
      router.push('/api/login');
    }, 2000);
  }
};

onMounted(() => {
  fetchUserFiles();
});

const deleteFile = async (fileId) => {
  try {
    const response = await axios.post(`${proxy.$apiBaseUrl}/api/deletefile/`, {
      id: fileId
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    toastDeleteMethod();
    fetchUserFiles();
  } catch (error) {
    console.error('Error deleting file:', error);
    toastErrorMethod();
  }
};

const openFile = async (fileId, fileFormat) => {
  try {
    if (fileFormat.toLowerCase() !== 'pdf') {
      toastOpenErrorMethod();
      return; // 直接返回，不继续执行删除操作
    }

    const url = `${proxy.$apiBaseUrl}/api/openfile/${fileId}/`;
    toastOpenMethod();
    setTimeout(() => {
      window.open(url, '_blank');
    }, 1500);
  } catch (error) {
    console.log(error);
    console.error('Error opening file:', error);
    toastOpenErrorMethod();
  }
};

const fileInput = ref(null);


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

const toastErrorMethod = () => {
    toast.error("Upload failed", {
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
  console.log(formData.value);
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
  localStorage.removeItem('username');
  router.push({
            path: '/api/login',
        });
};

</script>