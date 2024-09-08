<template>
  <div class="flex min-h-full flex-1 flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-6xl font-bold leading-9 tracking-tight text-white">Organoid Chat</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-[630px]">
      <div class="bg-white px-6 shadow sm:rounded-lg sm:px-6">
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
            <div class="flex text-blue-700 text-4xl font-semibold w-full justify-center items-center">Register</div>
          </div>

          <form @submit.prevent="RegisterUser">
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

            <div class="py-5">
              <button type="submit"
                class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign
                Up</button>
            </div>
          </form>

          <div class="flex items-center justify-between">
            <div class="flex text-gray-400 text-lg w-full justify-center items-center">Made by ustc-mbit research group.
            </div>
          </div>
        
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
const router = useRouter();

// 定义响应式变量
const username = ref('');
const password = ref('');
import { useToast } from 'vue-toastification';
const toast = useToast();
const toastSuccessMethod = () => {
    toast.info("Register successfully!", {
    position: "top-right",
    timeout: 1000,
    closeOnClick: true,
    icon: true,
});
};

const toastErrorMethod = () => {
    toast.error("Same username exists", {
    position: "top-right",
    timeout: 4000,
    closeOnClick: true,
    icon: true,
});
};
import { getCurrentInstance } from 'vue';
const { proxy } = getCurrentInstance();  // 获取实例代理
// 注册用户函数
const RegisterUser = async () => {
  console.log(username.value);
  console.log(password.value);
  try {
    const response = await axios.post(`${proxy.$apiBaseUrl}/api/register/`, {
      username: username.value,
      password: password.value,
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    toastSuccessMethod();

    setTimeout(() => {
      router.push('/api/login');  // 假设你的登录页面的路径是 /login
    }, 1000);
  } catch (error) {
    toastErrorMethod();
  }
};

</script>