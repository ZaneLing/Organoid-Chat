<template>
    <div class="flex flex-row">

        <div class="flex flex-none h-screen w-72 flex-col bg-blue-800">
            <div class="flex grow flex-col gap-y-5 overflow-y-auto px-6">
                <div class="flex h-16 shrink-0 items-center">
                    <div class="h-8 basis-1/4">
                        <img class="w-16 rounded-full" src="./assets/ustc-logo.png" alt="Your Company" />
                    </div>
                    <div class="h-1 basis-3/4 text-center text-lg text-white font-semibold ">Organoid Chat</div>
                </div>
                <nav class="flex flex-1 flex-col">
                    <ul role="list" class="flex flex-1 flex-col gap-y-7">
                        <li>
                            <ul role="list" class="-mx-2 space-y-1">
                                <li v-for="(item, index) in navigation" :key="item.name">
                                    <a :href="item.href"
                                        :class="[item.current ? 'bg-blue-400 hover:text-blue-600 text-white' : 'text-white hover:text-blue-500 hover:bg-white', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
                                        @click="setActiveItem(index)">
                                        <component :is="item.icon" class="h-6 w-6 shrink-0" aria-hidden="true" />
                                        {{ item.name }}
                                    </a>
                                </li>
                            </ul>
                        </li>
                        
                        <li class="-mx-6 mt-auto">
                            <a href="/base/settings"
                                class="flex items-center gap-x-4 px-6 py-3 text-sm font-semibold leading-6 text-white hover:text-blue-500 hover:bg-white hover:rounded-md">
                                <UserCircleIcon class="h-8 w-8 rounded-full bg-blue-700" />
                                
                                <span aria-hidden="true">{{username || 'Guest'}}</span>
                            </a>
                        </li>
                    </ul>
                </nav>
            </div>
        </div>

        <div class="flex flex-1 h-screen flex-col">
            <router-view></router-view>
        </div>

    </div>
</template>
  
<script setup>

import { ref, onMounted } from 'vue';


const username = ref('');

onMounted(()=>{
    username.value = localStorage.getItem('username');
})

function setActiveItem(selectedIndex) {
    this.navigation.forEach((item, index) => {
        item.current = (index === selectedIndex)
    });
}

const navigation = [
    { name: 'Home', href: '/base/home', icon: ServerIcon, current: false },
    { name: 'New chat', href: '/base/chat', icon: ChatBubbleBottomCenterTextIcon, current: false },
    { name: 'Userspace', href: '/base/userspace', icon: FolderIcon, current: false },
    { name: 'Knowledge Graph', href: '/base/kg', icon: SignalIcon, current: false },
    { name: 'History', href: '/base/history', icon: ChatBubbleLeftEllipsisIcon, current: false },
    { name: 'Settings', href: '/base/settings', icon: Cog6ToothIcon, current: false },
]

import { ChatBubbleLeftEllipsisIcon } from "@heroicons/vue/24/outline";


import {
    Cog6ToothIcon,
    FolderIcon,
    ServerIcon,
    SignalIcon,
    UserCircleIcon,
    ChatBubbleBottomCenterTextIcon
} from '@heroicons/vue/24/outline'

</script>