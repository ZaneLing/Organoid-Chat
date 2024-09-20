<template>
    <div class="flex flex-row">
        <div class="flex flex-1 h-screen flex-col bg-blue-300">
            <router-view></router-view>

            <!--icons-->
            <div class="mt-8 sm:mx-auto sm:max-w-[650px]">
                <div class="bg-white shadow sm:rounded-lg sm:px-5 py-4">
                    <div class="flex w-full h-32 justify-center items-center gap-6 px-20">
                        <img class="rounded-full h-24 w-24" src="../assets/ustc.jpg" alt="USTC">
                        <img class="rounded-full h-16" src="../assets/mbit.jpg" alt="mbit">
                    </div>
                    <div class="flex h-20 justify-center items-center gap-2">
                        <img class="bg-white h-20" src="../assets/sgy.png" alt="sgy">
                    </div>
                    <div class="flex h-20 justify-center items-center gap-2">
                        <img class="bg-white rounded-full h-20" src="../assets/ygs-long.jpg" alt="ygs">
                    </div>
                </div>
            </div>

            <!--title-->
            <div class="flex w-full h-48 pt-5 bg-blue-300 justify-center items-center font-semibold">
                <div class="flex justify-center h-40 rounded-lg">
                    <img class="rounded-full" src="../assets/OC-logo.jpg" alt="oclogo">
                </div>
                
            </div>

            <!--list-->
            <div class="flex-1 w-full bg-blue-300 flex-row pt-32 justify-center text-center px-20">
                <div class="flex-1 px-10 flex-row">
                    <div class="grid grid-cols-3 gap-6">
                        <div v-for="question in questions" :key="question.id"
                            class="relative flex items-center space-x-3 rounded-lg border bg-blue-800 border-blue-200 px-6 py-5 shadow-xl focus-within:ring-2 focus-within:ring-blue-500 focus-within:ring-offset-2 hover:border-blue-400"
                            @click="goToChat(question.id)">
                            <div class="min-w-0 flex-1">
                                <a href="#" class="focus:outline-none">
                                    <span class="absolute inset-0" aria-hidden="true" />
                                    <p class="truncate text-2xl font-semibold text-white">{{ question.name }}</p>
                                    <p class="truncate text-sm font-sans text-blue-300">{{ question.content }}</p>
                                </a>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>

import { useRouter } from 'vue-router';

const router = useRouter();

const goToChat = (id) => {
    if (id == '1') {
        router.push({
            path: '/base/userspace',
        });
    }
    else if (id == '2') {
        router.push({
            path: '/base/kg',
        });
    }
    else if (id == '3') {
        router.push({
            path: '/base/start',
        });
    }
};

import { ref } from 'vue'

const questions = ref([
    {
        name: 'FileSpace',
        id: '1',
        content: 'Upload your organoid files'
    },
    {
        name: 'Knowledge Graph',
        id: '2',
        content: 'Generate Knowledge Graph'
    },
    {
        name: 'Chat',
        id: '3',
        content: 'Q&A'
    }
])

</script>