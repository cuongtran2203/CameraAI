<template>
    <div
        class="bg-background-light dark:bg-background-dark font-display text-slate-900 dark:text-slate-100 antialiased h-screen overflow-hidden">
        <div class="relative flex h-full w-full flex-col">
            <!-- Top Navigation Bar -->
            <header
                class="flex items-center justify-between whitespace-nowrap border-b border-primary/20 px-10 py-3 bg-background-light dark:bg-background-dark">
                <div class="flex items-center gap-8">
                    <div class="flex items-center gap-4 text-primary">
                        <div class="size-6">
                            <span class="material-symbols-outlined text-3xl">videocam</span>
                        </div>
                        <h2 class="text-slate-900 dark:text-slate-100 text-lg font-bold leading-tight tracking-tight">
                            Camera Analyst</h2>
                    </div>
                    <nav class="flex items-center gap-8">
                        <router-link to="/"
                            class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary text-sm font-medium transition-colors">Dashboard</router-link>
                        <router-link to="/customer-analytics"
                            class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary text-sm font-medium transition-colors">Analytics</router-link>
                        <span class="text-primary text-sm font-bold border-b-2 border-primary pb-1">Configuration</span>
                        <router-link to="/camera-config"
                            class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary text-sm font-medium transition-colors">System</router-link>
                    </nav>
                </div>
                <div class="flex flex-1 justify-end gap-6 items-center">
                    <label class="flex flex-col min-w-40 h-10 max-w-64">
                        <div
                            class="flex w-full flex-1 items-stretch rounded-xl h-full bg-slate-200 dark:bg-primary/10 border border-slate-300 dark:border-primary/20">
                            <div class="text-slate-500 dark:text-primary/60 flex items-center justify-center pl-4">
                                <span class="material-symbols-outlined text-xl">search</span>
                            </div>
                            <input
                                class="form-input flex w-full min-w-0 flex-1 border-none bg-transparent focus:ring-0 text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-primary/40 px-3 text-sm"
                                placeholder="Search cameras..." value="" />
                        </div>
                    </label>
                    <div class="flex gap-2">
                        <button
                            class="flex items-center justify-center rounded-xl h-10 w-10 bg-slate-200 dark:bg-primary/20 text-slate-700 dark:text-slate-200 hover:bg-primary/30 transition-colors">
                            <span class="material-symbols-outlined">notifications</span>
                        </button>
                        <button
                            class="flex items-center justify-center rounded-xl h-10 w-10 bg-slate-200 dark:bg-primary/20 text-slate-700 dark:text-slate-200 hover:bg-primary/30 transition-colors">
                            <span class="material-symbols-outlined">settings</span>
                        </button>
                    </div>
                    <div
                        class="bg-primary/20 border border-primary/40 rounded-full size-10 flex items-center justify-center overflow-hidden">
                        <img class="w-full h-full object-cover" data-alt="User profile avatar portrait"
                            src="https://lh3.googleusercontent.com/aida-public/AB6AXuCD-u6ErQKsIFyISUBHkISMnYBFW6dfGPpTrJdbTmgbGgnoFwyNgwzWqnuCS5Yj8p_gBR1ZUiFM9wlwf4gVhG8-PFcTdp9IZJH65lvAebvPXKmKyV3IZ_lgZhIF7C46aEYza4Fu6aESNCMnBMHv3bS7cXfgx6Gt8LUtFpGTbcYE9Gvn-Z5GuSH-U5u5nfQCAirn5RrxFS23YgwdlUsYOhYFqlumNw5p9CO5N5D_DBLj8qLQdIfTdnDMlGwKLf1jOzMWzN74LLez-aA" />
                    </div>
                </div>
            </header>
            <div class="flex flex-1 overflow-hidden h-[calc(100vh-64px)]">
                <!-- Sidebar: Camera List -->
                <aside
                    class="w-72 border-r border-primary/20 bg-background-light dark:bg-background-dark p-6 flex flex-col gap-6 min-h-0">
                    <div class="flex flex-col gap-1">
                        <h1 class="text-slate-900 dark:text-slate-100 text-lg font-bold">Camera List</h1>
                        <p class="text-primary text-sm font-medium">
                            {{ onlineCount }} Online • {{ offlineCount }} Offline
                        </p>
                    </div>
                    <div v-if="camerasError" class="text-red-400 text-xs px-2">{{ camerasError }}</div>
                    <div class="flex flex-col gap-2 overflow-y-auto pr-2 custom-scrollbar">
                        <!-- AI Stream: DeepStream processed output -->
                        <div
                            class="flex items-center gap-3 px-4 py-3 rounded-xl border border-primary/40 hover:bg-primary/10 transition-colors cursor-pointer group"
                            :class="selectedStreamTab === 'ai' ? 'bg-primary text-white shadow-lg shadow-primary/20' : ''"
                            @click="selectedStreamTab = 'ai'; stopStream(); connectDeepStream()">
                            <span class="material-symbols-outlined">psychology</span>
                            <div class="flex flex-col">
                                <p class="text-sm font-bold">AI Processed Stream</p>
                                <p class="text-[10px] opacity-80 uppercase tracking-wider font-semibold">DeepStream YOLO</p>
                            </div>
                            <span class="ml-auto material-symbols-outlined text-xs opacity-60">smart_toy</span>
                        </div>
                        <!-- Camera streams -->
                        <div v-if="isLoadingCameras" class="flex items-center gap-2 px-4 py-3 text-slate-400 text-xs">
                            <span class="material-symbols-outlined animate-spin">progress_activity</span>
                            Đang tải...
                        </div>
                        <div v-for="camera in cameras" :key="camera.id"
                            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors cursor-pointer group"
                            :class="selectedCameraId === camera.id && selectedStreamTab === 'camera'
                                ? 'bg-primary text-white shadow-lg shadow-primary/20'
                                : 'hover:bg-primary/10'"
                            @click="selectCamera(camera)">
                            <span :class="['material-symbols-outlined', camera.is_active === false ? 'text-slate-500' : '']">
                                {{ camera.is_active !== false ? 'videocam' : 'videocam_off' }}
                            </span>
                            <div class="flex flex-col min-w-0">
                                <p class="text-sm font-bold truncate">{{ camera.name || camera.code }}</p>
                                <p class="text-[10px] opacity-80 uppercase tracking-wider font-semibold">
                                    {{ camera.is_active !== false ? 'Recording' : 'Offline' }}
                                </p>
                            </div>
                        </div>
                    </div>
                    <button
                        class="mt-auto flex items-center justify-center gap-2 w-full rounded-xl py-3 bg-primary/10 border-2 border-dashed border-primary/30 text-primary hover:bg-primary/20 transition-all font-bold text-sm">
                        <span class="material-symbols-outlined">add_circle</span>
                        <span>Add New Camera</span>
                    </button>
                </aside>
                <!-- Main Content Area -->
                <main class="flex-1 flex flex-col bg-slate-50 dark:bg-[#1a110d] min-h-0 h-[calc(100vh-64px)]">
                    <!-- Header Section -->
                    <div class="flex flex-wrap justify-between items-center gap-4 p-8 shrink-0">
                        <div class="flex flex-col gap-1">
                            <h2 class="text-slate-900 dark:text-slate-100 text-3xl font-black tracking-tight">Camera
                                Configuration</h2>
                            <div class="flex items-center gap-2">
                                <span class="size-2 rounded-full bg-green-500 animate-pulse"></span>
                            </div>
                        </div>
                        <div class="flex gap-3">
                            <button
                                class="flex items-center justify-center rounded-xl h-11 px-6 bg-slate-200 dark:bg-primary/10 text-slate-700 dark:text-slate-300 text-sm font-bold hover:bg-primary/20 transition-all">
                                Cancel
                            </button>
                            <button v-if="selectedStreamTab !== 'ai'" @click="saveCamera"
                                class="flex items-center justify-center rounded-xl h-11 px-8 bg-primary text-white text-sm font-bold hover:brightness-110 shadow-lg shadow-primary/30 transition-all">
                                Save Changes
                            </button>
                        </div>
                    </div>
                    <!-- Tabs -->
                    <div class="px-8 shrink-0">
                        <div class="flex border-b border-primary/10 gap-8">
                            <button class="flex items-center gap-2 border-b-2 border-primary text-primary pb-4 px-2">
                                <span class="material-symbols-outlined text-xl">polyline</span>
                                <span class="text-sm font-bold">Video Feed &amp; ROI</span>
                            </button>
                            <button
                                class="flex items-center gap-2 border-b-2 border-transparent text-slate-500 dark:text-slate-400 hover:text-primary pb-4 px-2 transition-colors">
                                <span class="material-symbols-outlined text-xl">psychology</span>
                                <span class="text-sm font-bold">AI Model Parameters</span>
                            </button>
                            <button
                                class="flex items-center gap-2 border-b-2 border-transparent text-slate-500 dark:text-slate-400 hover:text-primary pb-4 px-2 transition-colors">
                                <span class="material-symbols-outlined text-xl">lan</span>
                                <span class="text-sm font-bold">Network Settings</span>
                            </button>
                        </div>
                    </div>
                    <!-- Configuration Content -->
                    <div class="p-8 h-[calc(100vh-200px)] overflow-hidden">
                        <div class="flex gap-8 h-full min-h-0">
                            <!-- Left: ROI and Video Preview -->
                            <div class="flex-1 flex flex-col gap-6 overflow-y-auto custom-scrollbar h-full">
                                <div class="bg-slate-900 dark:bg-black rounded-2xl overflow-hidden relative border border-primary/30 shadow-2xl shrink-0">
                                    <!-- Video Feed (Real Stream or AI Processed) -->
                                    <div class="w-full aspect-square max-h-[480px] mx-auto bg-slate-900 flex items-center justify-center relative group">

                                        <!-- ── AI Stream ── -->
                                        <template v-if="selectedStreamTab === 'ai'">
                                            <!-- Loading -->
                                            <div v-if="deepstreamLoading" class="absolute inset-0 flex items-center justify-center z-10 bg-slate-900/80">
                                                <div class="flex flex-col items-center gap-3">
                                                    <span class="material-symbols-outlined text-5xl text-primary animate-spin">progress_activity</span>
                                                    <span class="text-white text-sm font-bold">Đang kết nối AI stream...</span>
                                                </div>
                                            </div>
                                            <!-- Error -->
                                            <div v-else-if="deepstreamError && !deepstreamConnected" class="absolute inset-0 flex items-center justify-center z-10 bg-slate-900/80">
                                                <div class="flex flex-col items-center gap-3 text-center px-8">
                                                    <span class="material-symbols-outlined text-5xl text-red-400">smart_toy</span>
                                                    <span class="text-red-400 text-sm font-bold">{{ deepstreamError }}</span>
                                                    <button @click="connectDeepStream"
                                                        class="px-4 py-2 bg-red-500/20 border border-red-500/40 text-red-400 rounded-lg text-xs font-bold hover:bg-red-500/30 transition-all">
                                                        Thử lại
                                                    </button>
                                                </div>
                                            </div>
                                            <!-- Idle -->
                                            <div v-if="!deepstreamConnected && !deepstreamLoading && !deepstreamError"
                                                class="absolute inset-0 flex flex-col items-center justify-center gap-3 z-10">
                                                <span class="material-symbols-outlined text-6xl text-slate-600">psychology</span>
                                                <span class="text-slate-500 text-sm">AI Processed Stream</span>
                                                <button @click="connectDeepStream"
                                                    class="px-4 py-2 bg-primary/20 border border-primary/40 text-primary rounded-lg text-xs font-bold hover:bg-primary/30 transition-all">
                                                    Kết nối AI Stream
                                                </button>
                                            </div>
                                            <!-- Video -->
                                            <video ref="deepstreamVideoRef"
                                                class="w-full h-full object-cover"
                                                :class="{ 'opacity-0': !deepstreamConnected }"
                                                autoplay muted playsinline controls></video>
                                            <!-- Live badge -->
                                            <div v-if="deepstreamConnected"
                                                class="absolute top-4 left-4 bg-slate-900/80 backdrop-blur-md rounded-lg px-3 py-2 flex items-center gap-2 border border-primary/30 text-[10px] font-bold text-primary uppercase tracking-widest">
                                                <span class="relative flex h-2 w-2">
                                                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                                                    <span class="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
                                                </span>
                                                AI Live
                                            </div>
                                        </template>

                                        <!-- ── Camera Stream ── -->
                                        <template v-else>
                                            <!-- Loading overlay -->
                                            <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center z-10 bg-slate-900/80">
                                                <div class="flex flex-col items-center gap-3">
                                                    <span class="material-symbols-outlined text-5xl text-primary animate-spin">progress_activity</span>
                                                    <span class="text-white text-sm font-bold">Đang kết nối camera...</span>
                                                </div>
                                            </div>
                                            <!-- Error overlay -->
                                            <div v-else-if="errorMsg && !isConnected" class="absolute inset-0 flex items-center justify-center z-10 bg-slate-900/80">
                                                <div class="flex flex-col items-center gap-3 text-center px-8">
                                                    <span class="material-symbols-outlined text-5xl text-red-400">videocam_off</span>
                                                    <span class="text-red-400 text-sm font-bold">{{ errorMsg }}</span>
                                                    <button @click="connectStream"
                                                        class="px-4 py-2 bg-red-500/20 border border-red-500/40 text-red-400 rounded-lg text-xs font-bold hover:bg-red-500/30 transition-all">
                                                        Thử lại
                                                    </button>
                                                </div>
                                            </div>
                                            <!-- Video element -->
                                            <video ref="videoRef"
                                                class="w-full h-full object-cover"
                                                :class="{ 'opacity-0': !isConnected }"
                                                autoplay muted playsinline controls></video>
                                            <!-- Idle state (no stream) -->
                                            <div v-if="!isConnected && !isLoading && !errorMsg" class="absolute inset-0 flex flex-col items-center justify-center gap-3">
                                                <span class="material-symbols-outlined text-6xl text-slate-600">videocam_off</span>
                                                <span class="text-slate-500 text-sm">Chưa kết nối camera</span>
                                                <button @click="connectStream"
                                                    class="px-4 py-2 bg-primary/20 border border-primary/40 text-primary rounded-lg text-xs font-bold hover:bg-primary/30 transition-all">
                                                    Kết nối
                                                </button>
                                            </div>
                                            <!-- Drawing Overlay Mockup -->
                                            <svg class="absolute inset-0 w-full h-full pointer-events-none">
                                                <polygon fill="rgba(236, 91, 19, 0.2)" points="100,100 400,120 450,300 150,350"
                                                    stroke="#ec5b13" stroke-dasharray="8 4" stroke-width="3"></polygon>
                                                <circle cx="100" cy="100" fill="#ec5b13" r="6"></circle>
                                                <circle cx="400" cy="120" fill="#ec5b13" r="6"></circle>
                                                <circle cx="450" cy="300" fill="#ec5b13" r="6"></circle>
                                                <circle cx="150" cy="350" fill="#ec5b13" r="6"></circle>
                                                <text fill="#ec5b13" font-size="14" font-weight="bold" x="110" y="90">Entrance ROI</text>
                                                <circle cx="600" cy="200" fill="white" r="8" stroke="#ec5b13" stroke-width="2"></circle>
                                            </svg>
                                            <!-- Tool HUD -->
                                            <div class="absolute top-4 left-4 flex gap-2">
                                                <div class="bg-slate-900/80 backdrop-blur-md rounded-lg p-1 flex gap-1 border border-primary/30">
                                                    <button class="p-2 bg-primary text-white rounded-md flex items-center justify-center">
                                                        <span class="material-symbols-outlined text-sm">draw</span>
                                                    </button>
                                                    <button class="p-2 text-slate-300 hover:bg-slate-700 rounded-md flex items-center justify-center">
                                                        <span class="material-symbols-outlined text-sm">rectangle</span>
                                                    </button>
                                                    <button class="p-2 text-slate-300 hover:bg-slate-700 rounded-md flex items-center justify-center">
                                                        <span class="material-symbols-outlined text-sm">circle</span>
                                                    </button>
                                                    <div class="w-px bg-primary/20 mx-1"></div>
                                                    <button class="p-2 text-red-500 hover:bg-red-500/10 rounded-md flex items-center justify-center">
                                                        <span class="material-symbols-outlined text-sm">delete</span>
                                                    </button>
                                                </div>
                                                <div v-if="isConnected"
                                                    class="bg-slate-900/80 backdrop-blur-md rounded-lg px-3 py-2 flex items-center gap-2 border border-primary/30 text-[10px] font-bold text-primary uppercase tracking-widest">
                                                    <span class="relative flex h-2 w-2">
                                                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                                                        <span class="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
                                                    </span>
                                                    Live Stream
                                                </div>
                                            </div>
                                            <!-- Bottom Controls -->
                                            <div class="absolute bottom-4 right-4 flex gap-2">
                                                <button class="bg-slate-900/80 backdrop-blur-md p-2 rounded-lg text-white border border-primary/20 hover:bg-primary/20 transition-colors">
                                                    <span class="material-symbols-outlined">zoom_in</span>
                                                </button>
                                                <button class="bg-slate-900/80 backdrop-blur-md p-2 rounded-lg text-white border border-primary/20 hover:bg-primary/20 transition-colors">
                                                    <span class="material-symbols-outlined">fullscreen</span>
                                                </button>
                                            </div>
                                        </template>
                                    </div>
                                </div>
                                <div v-if="selectedStreamTab !== 'ai'" class="flex items-start gap-4 p-4 bg-primary/5 border border-primary/20 rounded-xl shrink-0">
                                    <span class="material-symbols-outlined text-primary">info</span>
                                    <div>
                                        <p class="text-sm font-bold text-slate-900 dark:text-slate-100">ROI Configuration Tip</p>
                                        <p class="text-xs text-slate-600 dark:text-slate-400 mt-1">Drawing specific Regions of Interest (ROI) helps the AI focus on critical areas like entrances or registers, reducing false positives and saving processing power.</p>
                                    </div>
                                </div>
                                <div v-if="selectedStreamTab !== 'ai'" class="bg-background-light dark:bg-background-dark p-6 rounded-2xl border border-primary/20 shadow-sm flex flex-col gap-6 shrink-0">
                                    <div>
                                        <h3 class="text-lg font-bold text-slate-900 dark:text-slate-100 mb-4 flex items-center gap-2">
                                            <span class="material-symbols-outlined text-primary">lan</span>
                                            Network Stream Settings
                                        </h3>
                                        <div class="flex flex-col gap-4">
                                            <div class="flex flex-col gap-2">
                                                <label class="text-sm font-semibold text-slate-600 dark:text-slate-400" for="camera-name">
                                                    Camera Name
                                                </label>
                                                <div class="flex w-full items-stretch rounded-xl h-11 bg-slate-200 dark:bg-primary/10 border border-slate-300 dark:border-primary/20">
                                                    <div class="text-slate-500 dark:text-primary/60 flex items-center justify-center pl-4">
                                                        <span class="material-symbols-outlined text-xl">videocam</span>
                                                    </div>
                                                    <input v-model="cameraName" class="form-input flex w-full min-w-0 flex-1 border-none bg-transparent focus:ring-0 text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-primary/40 px-3 text-sm"
                                                        id="camera-name"
                                                        placeholder="My Camera" />
                                                </div>
                                            </div>
                                            <div class="flex flex-col gap-2">
                                                <label class="text-sm font-semibold text-slate-600 dark:text-slate-400" for="rtsp-url">
                                                    RTSP Stream URL
                                                </label>
                                                <div class="flex w-full items-stretch rounded-xl h-11 bg-slate-200 dark:bg-primary/10 border border-slate-300 dark:border-primary/20">
                                                    <div class="text-slate-500 dark:text-primary/60 flex items-center justify-center pl-4">
                                                        <span class="material-symbols-outlined text-xl">link</span>
                                                    </div>
                                                    <input v-model="rtspUrl" class="form-input flex w-full min-w-0 flex-1 border-none bg-transparent focus:ring-0 text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-primary/40 px-3 text-sm"
                                                        id="rtsp-url"
                                                        placeholder="rtsp://admin:password@192.168.1.104:554/stream" />
                                                    <button @click="connectStream"
                                                        class="flex items-center justify-center px-4 bg-primary text-white rounded-r-xl hover:brightness-110 transition-all shrink-0">
                                                        <span class="material-symbols-outlined text-xl">play_arrow</span>
                                                    </button>
                                                </div>
                                                <!-- Status -->
                                                <div v-if="isConnected" class="flex items-center gap-2 text-green-600 text-xs font-bold">
                                                    <span class="relative flex h-2 w-2">
                                                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-500 opacity-75"></span>
                                                        <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                                                    </span>
                                                    Kết nối thành công
                                                </div>
                                                <div v-else-if="errorMsg" class="flex items-center gap-2 text-red-500 text-xs font-bold">
                                                    <span class="material-symbols-outlined text-sm">error</span>
                                                    {{ errorMsg }}
                                                </div>
                                                <div v-else-if="isLoading" class="flex items-center gap-2 text-primary text-xs font-bold">
                                                    <span class="material-symbols-outlined text-sm animate-spin">progress_activity</span>
                                                    Đang kết nối...
                                                </div>
                                                <p class="text-[10px] text-slate-500 italic">
                                                    Nhập link RTSP đầy đủ (protocol://user:pass@ip:port/path), ví dụ: rtsp://admin:password@192.168.1.104:554/stream
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- Right: AI Parameters Panel -->
                            <div class="w-1/3 flex flex-col gap-6 overflow-y-auto custom-scrollbar h-full">
                                <div class="bg-background-light dark:bg-background-dark p-6 rounded-2xl border border-primary/20 shadow-sm flex flex-col gap-8 shrink-0">
                                    <div>
                                        <h3 class="text-lg font-bold text-slate-900 dark:text-slate-100 mb-4 flex items-center gap-2">
                                            <span class="material-symbols-outlined text-primary">face</span>
                                            Face ID Confidence
                                        </h3>
                                        <div class="flex flex-col gap-4">
                                            <div class="flex justify-between items-center text-sm font-semibold">
                                                <span class="text-slate-600 dark:text-slate-400">Detection Threshold</span>
                                                <span class="text-primary">85%</span>
                                            </div>
                                            <input class="w-full h-1.5 bg-slate-200 dark:bg-primary/10 rounded-lg appearance-none cursor-pointer accent-primary" type="range" />
                                            <p class="text-[10px] text-slate-500 italic">High threshold reduces false positives but might miss some faces in low light.</p>
                                        </div>
                                    </div>
                                    <div class="h-px bg-primary/10"></div>
                                    <div>
                                        <h3 class="text-lg font-bold text-slate-900 dark:text-slate-100 mb-4 flex items-center gap-2">
                                            <span class="material-symbols-outlined text-primary">directions_run</span>
                                            HAR (Human Activity Recognition)
                                        </h3>
                                        <div class="flex flex-col gap-5">
                                            <div class="flex flex-col gap-3">
                                                <div class="flex justify-between items-center text-sm font-semibold">
                                                    <span class="text-slate-600 dark:text-slate-400">Motion Sensitivity</span>
                                                    <span class="text-primary">62%</span>
                                                </div>
                                                <input class="w-full h-1.5 bg-slate-200 dark:bg-primary/10 rounded-lg appearance-none cursor-pointer accent-primary" type="range" />
                                            </div>
                                            <div class="space-y-3">
                                                <label class="flex items-center justify-between cursor-pointer group">
                                                    <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Loitering Detection</span>
                                                    <div class="relative inline-flex items-center">
                                                        <input checked="" class="sr-only peer" type="checkbox" />
                                                        <div class="w-11 h-6 bg-slate-300 dark:bg-primary/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                                                    </div>
                                                </label>
                                                <label class="flex items-center justify-between cursor-pointer group">
                                                    <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Intrusion Alert</span>
                                                    <div class="relative inline-flex items-center">
                                                        <input checked="" class="sr-only peer" type="checkbox" />
                                                        <div class="w-11 h-6 bg-slate-300 dark:bg-primary/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                                                    </div>
                                                </label>
                                                <label class="flex items-center justify-between cursor-pointer group">
                                                    <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Crowd Density Monitor</span>
                                                    <div class="relative inline-flex items-center">
                                                        <input class="sr-only peer" type="checkbox" />
                                                        <div class="w-11 h-6 bg-slate-300 dark:bg-primary/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                                                    </div>
                                                </label>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="h-px bg-primary/10"></div>
                                    <div>
                                        <h3 class="text-lg font-bold text-slate-900 dark:text-slate-100 mb-4 flex items-center gap-2">
                                            <span class="material-symbols-outlined text-primary">storage</span>
                                            Storage Management
                                        </h3>
                                        <div class="p-3 bg-slate-100 dark:bg-primary/5 rounded-xl border border-primary/10">
                                            <div class="flex justify-between items-center mb-2">
                                                <span class="text-[10px] font-bold uppercase text-slate-500">Local Cache (SSD)</span>
                                                <span class="text-[10px] font-bold text-primary">78% Full</span>
                                            </div>
                                            <div class="w-full h-1 bg-slate-200 dark:bg-primary/10 rounded-full overflow-hidden">
                                                <div class="h-full bg-primary" style="width: 78%"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Hls from 'hls.js'
import { API_BASE_URL, MEDIAMTX_URL } from '@/config/api.js'

// --- State ---
const videoRef = ref(null)
const rtspUrl = ref('')
const isLoading = ref(false)
const isConnected = ref(false)
const errorMsg = ref('')
const cameraName = ref('Camera 1')
const selectedStreamTab = ref('camera') // 'camera' | 'ai'
const cameras = ref([])
const selectedCameraId = ref(null)
const isLoadingCameras = ref(false)
const camerasError = ref('')
const deepstreamConnected = ref(false)
const deepstreamLoading = ref(false)
const deepstreamError = ref('')
const deepstreamVideoRef = ref(null)
let hlsInstance = null
let dsHlsInstance = null
let camerasRefreshTimer = null

// Auth token from localStorage
const getToken = () => localStorage.getItem('auth_token') || ''

// --- Fetch cameras from backend API ---
const fetchCameras = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/v1/cameras?page_size=50`, {
      headers: { Authorization: `Bearer ${getToken()}` }
    })
    if (!res.ok) throw new Error('Failed to fetch cameras')
    cameras.value = await res.json()
    camerasError.value = ''
  } catch (e) {
    camerasError.value = 'Không thể tải danh sách camera'
    console.error(e)
  }
}

// --- Select a camera ---
const selectCamera = (camera) => {
  selectedCameraId.value = camera.id
  cameraName.value = camera.name || camera.code || 'Camera'
  rtspUrl.value = camera.rtsp_url || ''
  isConnected.value = false
  isLoading.value = false
  errorMsg.value = ''
  stopStream()
  // Auto-connect if RTSP URL available
  if (rtspUrl.value) {
    setTimeout(() => connectStream(), 200)
  }
}

// --- Convert input URL to playable HLS URL ---
const getStreamName = (url) => {
  return btoa(encodeURIComponent(url)).replace(/[/+=]/g, '_')
}

const toFrontendHlsProxy = (pathname) => {
  // If path already starts with /hls/, don't double-prefix
  const cleanPath = pathname.replace(/^\//, '')
  if (cleanPath.startsWith('hls/')) {
    return `${window.location.origin}/${cleanPath}`
  }
  return `${window.location.origin}/hls/${cleanPath}`
}

const normalizeExistingHlsUrl = (url) => {
  try {
    const u = new URL(url)
    // Common old format: http://localhost:8888/ds-test/hls.m3u8
    if (u.pathname.endsWith('/hls.m3u8')) {
      return toFrontendHlsProxy(u.pathname.replace('/hls.m3u8', '/index.m3u8'))
    }
    // MediaMTX canonical format: /<path>/index.m3u8
    if (u.pathname.endsWith('/index.m3u8') || u.pathname.endsWith('.m3u8')) {
      return toFrontendHlsProxy(u.pathname)
    }
  } catch (_) {
    // not a full URL, fallback below
  }
  return null
}

const getHlsUrl = (url) => {
  // If user already entered an HLS URL, normalize it to frontend proxy path
  if (url?.includes('.m3u8')) {
    const normalized = normalizeExistingHlsUrl(url)
    if (normalized) return normalized
  }

  // Otherwise treat as RTSP-like source and map to MediaMTX on-demand path
  const streamName = getStreamName(url)
  return toFrontendHlsProxy(`/${streamName}/index.m3u8`)
}

// --- DeepStream AI-processed stream URL ---
const getDeepStreamHlsUrl = () => {
  return toFrontendHlsProxy('/ds-test/index.m3u8')
}

// --- Stop current stream ---
const stopStream = () => {
  if (hlsInstance) {
    hlsInstance.destroy()
    hlsInstance = null
  }
  if (videoRef.value) {
    videoRef.value.src = ''
    videoRef.value.removeAttribute('src')
    videoRef.value.load()
  }
  isConnected.value = false
  isLoading.value = false
  errorMsg.value = ''
}

const stopDeepStream = () => {
  if (dsHlsInstance) {
    dsHlsInstance.destroy()
    dsHlsInstance = null
  }
  if (deepstreamVideoRef.value) {
    deepstreamVideoRef.value.src = ''
    deepstreamVideoRef.value.removeAttribute('src')
    deepstreamVideoRef.value.load()
  }
  deepstreamConnected.value = false
  deepstreamLoading.value = false
  deepstreamError.value = ''
}

// --- Connect to RTSP stream via MediaMTX ---
const connectStream = async () => {
  if (!rtspUrl.value.trim()) {
    errorMsg.value = 'Vui lòng nhập RTSP URL'
    return
  }
  if (!videoRef.value) {
    errorMsg.value = 'Video player chưa sẵn sàng'
    return
  }

  stopStream()
  isLoading.value = true
  errorMsg.value = ''

  const hlsUrl = getHlsUrl(rtspUrl.value)
  await new Promise(resolve => setTimeout(resolve, 1500))

  if (videoRef.value.canPlayType('application/vnd.apple.mpegurl')) {
    videoRef.value.src = hlsUrl
    videoRef.value.addEventListener('loadedmetadata', () => {
      isLoading.value = false
      isConnected.value = true
      videoRef.value.play().catch(() => {})
    }, { once: true })
    videoRef.value.addEventListener('error', tryHlsJs, { once: true })
    return
  }
  tryHlsJs()
}

const tryHlsJs = () => {
  if (!Hls.isSupported()) {
    errorMsg.value = 'Trình duyệt không hỗ trợ HLS. Vui lòng dùng Safari hoặc Chrome.'
    isLoading.value = false
    return
  }
  const hlsUrl = getHlsUrl(rtspUrl.value)
  hlsInstance = new Hls({ enableWorker: true, lowLatencyMode: true, backBufferLength: 30 })
  hlsInstance.loadSource(hlsUrl)
  hlsInstance.attachMedia(videoRef.value)
  hlsInstance.on(Hls.Events.MANIFEST_PARSED, () => {
    isLoading.value = false
    isConnected.value = true
    videoRef.value.play().catch(() => {})
  })
  hlsInstance.on(Hls.Events.ERROR, (_, data) => {
    if (data.fatal) {
      errorMsg.value = `Lỗi stream: ${data.details || 'Không thể kết nối camera'}`
      isLoading.value = false
      isConnected.value = false
    }
  })
}

// --- Connect to DeepStream AI-processed stream ---
const connectDeepStream = async () => {
  if (!deepstreamVideoRef.value) return
  stopDeepStream()
  deepstreamLoading.value = true
  deepstreamError.value = ''
  const hlsUrl = getDeepStreamHlsUrl()
  await new Promise(resolve => setTimeout(resolve, 2000))
  if (deepstreamVideoRef.value.canPlayType('application/vnd.apple.mpegurl')) {
    deepstreamVideoRef.value.src = hlsUrl
    deepstreamVideoRef.value.addEventListener('loadedmetadata', () => {
      deepstreamLoading.value = false
      deepstreamConnected.value = true
      deepstreamVideoRef.value.play().catch(() => {})
    }, { once: true })
    deepstreamVideoRef.value.addEventListener('error', tryDsHlsJs, { once: true })
    return
  }
  tryDsHlsJs()
}

const tryDsHlsJs = () => {
  if (!Hls.isSupported()) {
    deepstreamError.value = 'Trình duyệt không hỗ trợ HLS'
    deepstreamLoading.value = false
    return
  }
  const hlsUrl = getDeepStreamHlsUrl()
  dsHlsInstance = new Hls({ enableWorker: true, lowLatencyMode: true, backBufferLength: 30 })
  dsHlsInstance.loadSource(hlsUrl)
  dsHlsInstance.attachMedia(deepstreamVideoRef.value)
  dsHlsInstance.on(Hls.Events.MANIFEST_PARSED, () => {
    deepstreamLoading.value = false
    deepstreamConnected.value = true
    deepstreamVideoRef.value.play().catch(() => {})
  })
  dsHlsInstance.on(Hls.Events.ERROR, (_, data) => {
    if (data.fatal) {
      deepstreamError.value = `Lỗi stream: ${data.details || 'Không thể kết nối AI stream'}`
      deepstreamLoading.value = false
      deepstreamConnected.value = false
    }
  })
}

// --- Save camera to backend API ---
const saveCamera = async () => {
  if (!rtspUrl.value.trim() || !cameraName.value.trim()) {
    errorMsg.value = 'Vui lòng nhập đầy đủ thông tin'
    return
  }
  try {
    // Use existing camera's branch_id if available, otherwise use default
    const existingCamera = cameras.value.find(c => c.id === selectedCameraId.value)
    const branchId = existingCamera?.branch_id || '00000000-0000-0000-0000-000000000001'

    if (selectedCameraId.value && existingCamera) {
      // Update existing camera
      const res = await fetch(`${API_BASE_URL}/v1/cameras/${selectedCameraId.value}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${getToken()}`
        },
        body: JSON.stringify({
          name: cameraName.value,
          rtsp_url: rtspUrl.value,
        })
      })
      if (!res.ok) throw new Error('Failed to update camera')
    } else {
      // Create new camera
      const res = await fetch(`${API_BASE_URL}/v1/cameras`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${getToken()}`
        },
        body: JSON.stringify({
          name: cameraName.value,
          code: `CAM-${Date.now()}`,
          rtsp_url: rtspUrl.value,
          branch_id: branchId,
          stream_type: rtspUrl.value?.includes('.m3u8') ? 'hls' : 'rtsp',
          ai_enabled: { face: true, action: true, food: true }
        })
      })
      if (!res.ok) throw new Error('Failed to save camera')
    }
    await fetchCameras()
    alert(`Đã lưu camera "${cameraName.value}" thành công!`)
  } catch (e) {
    alert(`Lỗi khi lưu: ${e.message}`)
  }
}

// Online camera count
const onlineCount = computed(() => cameras.value.filter(c => c.is_active !== false).length)
const offlineCount = computed(() => cameras.value.filter(c => c.is_active === false).length)

onMounted(() => {
  fetchCameras()
  camerasRefreshTimer = setInterval(fetchCameras, 30000)
})

onUnmounted(() => {
  stopStream()
  stopDeepStream()
  if (camerasRefreshTimer) clearInterval(camerasRefreshTimer)
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #ec5b1333;
    border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #ec5b1366;
}

.custom-scrollbar {
    scrollbar-width: thin;
    scrollbar-color: #ec5b1333 transparent;
}
</style>
