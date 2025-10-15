<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full text-center">
      <div class="mb-8">
        <h1 class="text-9xl font-bold text-gray-300">404</h1>
        <h2 class="text-2xl font-semibold text-gray-700 mb-4">页面未找到</h2>
        <p class="text-gray-500 mb-8">抱歉，您访问的页面不存在。</p>
      </div>
      
      <div class="space-y-4">
        <router-link 
          to="/" 
          class="inline-block bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200"
        >
          返回首页
        </router-link>
        
        <button 
          @click="$router.go(-1)"
          class="block w-full text-primary-600 hover:text-primary-700 font-medium py-2 transition-colors duration-200"
        >
          返回上一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 404 页面组件
</script>