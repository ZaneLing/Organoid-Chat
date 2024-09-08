<template>
  <div class="flex flex-1 bg-blue-600 h-auto">
    <div class="flex flex-col w-full">
      <div class="flex h-16">
        <header class="border-b border-white/5">
          <!-- Secondary navigation -->
          <nav class="flex overflow-x-auto py-4">
            <ul role="list"
              class="flex min-w-full flex-none gap-x-6 px-4 text-sm font-semibold leading-6 text-gray-400 sm:px-6 lg:px-8">
              <li v-for="item in secondaryNavigation" :key="item.name">
                <a :href="item.href" :class="item.current ? 'text-white font-bold text-lg' : 'text-gray-400'">{{ item.name
                }}</a>
              </li>
            </ul>
          </nav>
        </header>
      </div>

      <div class="flex flex-col divide-y divide-white/10">
        <div class="flex max-w-7xl gap-x-8 gap-y-10 px-4 py-3 sm:px-6 h-72 lg:px-8">
          <div>
            <h2 class="text-base font-semibold leading-7 text-white">Personal Information</h2>
          </div>

          <form @submit.prevent="updateUserInfo">
            <div class="flex flex-col h-44 px-10 gap-x-6 gap-y-6 sm:max-w-xl sm:grid-cols-6">
              <div class="flex flex-row gap-8">
              <div class="flex flex-col">
                <label for="first_name" class="block text-sm font-medium leading-6 text-white">First name</label>
                <div class="mt-2">
                  <input type="text" id="first_name" v-model="first_name"
                    class="block w-full rounded-md border-0 bg-white py-1.5 text-black shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6" />
                </div>
              </div>
              <div class="flex flex-col">
                <label for="last_name" class="block text-sm font-medium leading-6 text-white">Last name</label>
                <div class="mt-2">
                  <input type="text" id="last_name" v-model="last_name"
                    class="block w-full rounded-md border-0 bg-white py-1.5 text-black shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6" />
                </div>
              </div>
              </div>
              <div class="flex flex-col">
                <label for="email_address" class="block text-sm font-medium leading-6 text-white">Email address</label>
                <div class="mt-2">
                  <input id="email_address" type="email" v-model="email_address"
                    class="block w-full rounded-md border-0 bg-white py-1.5 text-black shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6" />
                </div>
              </div>
            </div>
            <div class="mt-4 flex px-10">
              <button type="submit"
                class="rounded-md bg-indigo-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500">Save</button>
            </div>
          </form>
        </div>

        <div class="flex max-w-7xl gap-x-8 gap-y-10 px-4 py-3 sm:px-6 md:grid-cols-3 lg:px-8">
          <div>
            <h2 class="text-base font-semibold leading-7 text-white">Change password</h2>
          </div>

          <form @submit.prevent="changePassword" class="flex flex-col">
            <div class="flex flex-col px-16 gap-x-6 gap-y-4 sm:max-w-xl sm:grid-cols-6">
              <div class="flex flex-col">
                <div class="flex flex-row gap-2">
                  <label for="currentPassword" class="block text-sm font-medium leading-6 text-white">Current
                    password</label>
                  <EyeIcon v-if="isPasswordVisible" type="button" @click="togglePasswordVisibility"
                    class="w-5 h-5 rounded-full bg-white" />
                  <EyeSlashIcon v-else type="button" @click="togglePasswordVisibility"
                    class="w-5 h-5 rounded-full bg-white" />
                </div>
                <div class="mt-2">
                  <input id="currentPassword" :type="isPasswordVisible ? ' text' : 'password'" v-model="currentPassword"
                    class="block w-full rounded-md border-0 text-black bg-white px-2 py-1.5 shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6" />
                </div>
              </div>

              <div class="flex flex-col">
                <label for="newPassword" class="block text-sm font-medium leading-6 text-white">New password</label>
                <div class="mt-2">
                  <input id="newPassword" :type="isPasswordVisible ? ' text' : 'password'" v-model="newPassword"
                    class="block w-full rounded-md border-0 bg-white py-1.5 px-2 text-black shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6" />
                </div>
              </div>

              <div class="flex flex-col">
                <label for="confirmPassword" class="block text-sm font-medium leading-6 text-white">Confirm
                  password</label>
                <div class="mt-2">
                  <input id="confirmPassword" :type="isPasswordVisible ? ' text' : 'password'" v-model="confirmPassword"
                    class="block w-full rounded-md border-0 bg-white py-1.5 px-2 text-black shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6" />
                </div>
              </div>

            </div>

            <div class="mt-8 flex px-10">
              <button type="submit"
                class="rounded-md bg-indigo-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500">Change</button>
            </div>
          </form>
        </div>


        <div class="flex flex-1 w-full px-20">
          <div class="flex flex-row gap-8 pt-10">
            <button @click="confirmDelete"
              class="rounded-md bg-red-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-400">
              Delete account</button>
            <div v-if="showPopup">
              <p class="flex font-semibold py-2 text-lg text-white">Confirm account deletion ?</p>
              <div class="flex flex-row gap-2">
                <button
                  class="rounded-md bg-red-300 w-20 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-400"
                  @click="deleteUser">Yes</button>
                <button
                  class="rounded-md bg-gray-300 w-20 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-500"
                  @click="cancelDelete">No</button>
              </div>
            </div>
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
const username = ref(localStorage.getItem('username'));
const showPopup = ref(false);
const router = useRouter();
const confirmDelete = () => {
  showPopup.value = true;
};
import { EyeIcon, EyeSlashIcon } from "@heroicons/vue/24/outline";
import { getCurrentInstance } from 'vue';
const { proxy } = getCurrentInstance();  // 获取实例代理


const cancelDelete = () => {
  showPopup.value = false;
};
import { useToast } from 'vue-toastification';
const toast = useToast();
const toastDeleteSuccessMethod = () => {
  toast.success("Delete successfully", {
    position: "top-right",
    timeout: 1500,
    closeOnClick: true,
    icon: true,
  });
};
const toastDeleteWrongsMethod = () => {
  toast.error("Delete failed", {
    position: "top-right",
    timeout: 3000,
    closeOnClick: true,
    icon: true,
  });
};

const toastWarnMethod = () => {
  toast.info("Please login first", {
    position: "top-right",
    timeout: 3000,
    closeOnClick: true,
    icon: true,
  });
};

const toastChangeSuccessMethod = () => {
  toast.success("Password Changes", {
    position: "top-right",
    timeout: 1500,
    closeOnClick: true,
    icon: true,
  });
};

const toastWrongPasswordMethod = () => {
  toast.error("Wrong Current Password", {
    position: "top-right",
    timeout: 3000,
    closeOnClick: true,
    icon: true,
  });
};
const toastConfirmPasswordMethod = () => {
  toast.error("Wrong Confirm Password", {
    position: "top-right",
    timeout: 3000,
    closeOnClick: true,
    icon: true,
  });
};

const toastUpdateMethod = () => {
  toast.success("Update info successfully", {
    position: "top-right",
    timeout: 1500,
    closeOnClick: true,
    icon: true,
  });
};
const toastWrongUpdateMethod = () => {
  toast.error("Update info failed", {
    position: "top-right",
    timeout: 3000,
    closeOnClick: true,
    icon: true,
  });
};

const deleteUser = async () => {
  console.log(username.value);
  if (username.value == null) {
    toastWarnMethod();
    setTimeout(() => {
      router.push('/api/login/');
    }, 2000);
    return;
  }
  try {
    const response = await axios.post(`${proxy.$apiBaseUrl}/api/deleteuser/`, {
      user: username.value
    }, {
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (response.status === 200) {
      localStorage.removeItem('username');
      toastDeleteSuccessMethod();
      setTimeout(() => {
        router.push('/api/login/');
      }, 1500);
    }
  } catch (error) {
    toastDeleteWrongsMethod();
    console.log(error);
  } finally {
    showPopup.value = false;
  }
};

const secondaryNavigation = [
  { name: 'Account', href: '#', current: true },
  { name: 'System(Disable)', href: '#', current: false },
]
const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');

const changePassword = async () => {
  if (username.value == null) {
    toastWarnMethod();
    setTimeout(() => {
      router.push('/api/login/');
    }, 2000);
  return;
  }

  try {
    const response = await axios.post(`${proxy.$apiBaseUrl}/api/changepassword/`, {
      user: username.value,
      currentPassword: currentPassword.value,
      newPassword: newPassword.value,
      confirmPassword: confirmPassword.value,
    }, {
      headers: {
        'Content-Type': 'application/json',
      }
    });
    console.log(response);
    toastChangeSuccessMethod();
    setTimeout(() => {
      router.push('/api/login/');
    }, 1500);
  } catch (error) {
    if (error.response) {
      if (error.response.data.error == 'current password wrong') {
        toastWrongPasswordMethod();
        return;
       }
      else if (error.response.data.error == 'two passwords not equal') {
        toastConfirmPasswordMethod();
        return;
      }
    } else {
      console.log(error);
    }
  }
};

const isPasswordVisible = ref(false);

const togglePasswordVisibility = () => {
  isPasswordVisible.value = !isPasswordVisible.value;
};

const first_name = ref('');
const last_name = ref('');
const email_address = ref('');

const updateUserInfo = async () => {
  try {
    const response = await axios.post(`${proxy.$apiBaseUrl}/api/updateuserinfo/`, {
      user: username.value,
      first_name: first_name.value,
      last_name: last_name.value,
      email_address: email_address.value,
    });

    console.log(response.data.message);
    toastUpdateMethod();
  } catch (error) {
    console.error(error.response.data.error);
    toastWrongUpdateMethod();
  }
};

</script>