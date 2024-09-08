<template>
    <div class="flex flex-col justify-center sm:px-6 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-md py-6">
            <h2 class="mt-6 text-center text-6xl font-bold leading-9 tracking-tight text-white">Organoid Chat</h2>
        </div>

        <div class="mt-8 sm:mx-auto sm:max-w-[630px]">
            <div class="bg-white shadow sm:rounded-lg sm:px-5">
                <div class="flex w-full h-32 justify-center items-center gap-6 px-20">
                    <img class="rounded-full h-24 w-24" src="../assets/ustc.jpg" alt="USTC">
                    <img class="rounded-full" src="../assets/mbit.jpg" alt="mbit">
                </div>
                <div class="flex h-20 justify-center items-center gap-2">
                    <img class="bg-white h-20" src="../assets/sgy.png" alt="sgy">
                </div>
                <div class="flex h-20 justify-center items-center gap-2">
                    <img class="bg-white rounded-full h-20" src="../assets/ygs-long.jpg" alt="ygs">
                </div>
                <div class="flex items-center justify-between">
                    <div class="flex text-blue-700 text-4xl font-semibold w-full justify-center items-center">Login
                    </div>
                </div>
                <form @submit.prevent="loginUser" class="gap-2">

                    <div>
                        <label for="email" class="block text-sm font-medium leading-6 text-gray-900">User Name</label>
                        <div class="mt-2">
                            <input v-model="username"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
                        </div>
                    </div>

                    <div>
                        <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
                        <div class="mt-2">
                            <input v-model="password" type="password"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
                        </div>
                    </div>

                    <div class="py-2">
                        <button type="submit"
                            class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign
                            In</button>
                    </div>
                </form>

                <div class="py-2">
                    <button @click="ToRegister" type="button"
                        class="flex w-full justify-center rounded-md bg-indigo-400 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign
                        Up</button>
                </div>

                <div class="flex items-center justify-between">
                    <div class="flex text-gray-400 text-lg w-full justify-center items-center">Made by ustc-mbit
                        research group.</div>
                </div>

            </div>
        </div>
    </div>
</template>
  
  
<script setup>
import { ref } from 'vue';
import axios from 'axios';
import router from '../router/index.js';
import { useRouter } from 'vue-router';

import { useToast } from "vue-toastification";

const username = ref('');
const password = ref('');

const toast = useToast();
const toastSuccessMethod = () => {
    toast.info("Login successfully!", {
    position: "top-right",
    timeout: 1500,
    closeOnClick: true,
    icon: true,
});
};
import { getCurrentInstance } from 'vue';
const { proxy } = getCurrentInstance();  // 获取实例代理
const toastErrorMethod = () => {
    toast.error("Username or password is incorrect!", {
    position: "top-right",
    timeout: 4000,
    closeOnClick: true,
    icon: true,
});
};

// 登录用户函数
const loginUser = async () => {
    try {
        const response = await axios.post(`${proxy.$apiBaseUrl}/api/login/`, {
            username: username.value,
            password: password.value,
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log(response.data);
        toastSuccessMethod();
        localStorage.setItem('username', response.data.username);
        localStorage.setItem('authToken', response.data.token);

        setTimeout(() => {
            window.location.href = '/base/home';
        }, 2000);
    } catch (error) {
        toastErrorMethod();
    }
};
// Redirect to the registration page
const ToRegister = () => {
    router.push('/api/register');
};
</script>