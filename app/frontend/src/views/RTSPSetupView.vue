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
                        <p class="text-primary text-sm font-medium">5 Online • 2 Offline</p>
                    </div>
                    <div class="flex flex-col gap-2 overflow-y-auto pr-2 custom-scrollbar">
                        <div
                            class="flex items-center gap-3 px-4 py-3 rounded-xl bg-primary text-white shadow-lg shadow-primary/20">
                            <span class="material-symbols-outlined">videocam</span>
                            <div class="flex flex-col">
                                <p class="text-sm font-bold">Main Entrance</p>
                                <p class="text-[10px] opacity-80 uppercase tracking-wider font-semibold">Recording</p>
                            </div>
                        </div>
                        <div
                            class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-primary/10 transition-colors cursor-pointer group">
                            <span
                                class="material-symbols-outlined text-slate-500 group-hover:text-primary">videocam</span>
                            <p class="text-slate-700 dark:text-slate-300 text-sm font-medium">Lobby North</p>
                        </div>
                        <div
                            class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-primary/10 transition-colors cursor-pointer group">
                            <span
                                class="material-symbols-outlined text-slate-500 group-hover:text-primary">videocam</span>
                            <p class="text-slate-700 dark:text-slate-300 text-sm font-medium">Parking Gate 1</p>
                        </div>
                        <div
                            class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-primary/10 transition-colors cursor-pointer group">
                            <span
                                class="material-symbols-outlined text-slate-500 group-hover:text-primary">videocam_off</span>
                            <p class="text-slate-400 dark:text-slate-500 text-sm font-medium italic">Warehouse A
                                (Offline)</p>
                        </div>
                        <div
                            class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-primary/10 transition-colors cursor-pointer group">
                            <span
                                class="material-symbols-outlined text-slate-500 group-hover:text-primary">videocam</span>
                            <p class="text-slate-700 dark:text-slate-300 text-sm font-medium">Exit West</p>
                        </div>
                        <div
                            class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-primary/10 transition-colors cursor-pointer group">
                            <span
                                class="material-symbols-outlined text-slate-500 group-hover:text-primary">videocam</span>
                            <p class="text-slate-700 dark:text-slate-300 text-sm font-medium">Breakroom</p>
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
                                <p class="text-slate-500 dark:text-primary/60 text-sm font-medium">Main Entrance - 4K IP
                                    Stream (192.168.1.104)</p>
                            </div>
                        </div>
                        <div class="flex gap-3">
                            <button
                                class="flex items-center justify-center rounded-xl h-11 px-6 bg-slate-200 dark:bg-primary/10 text-slate-700 dark:text-slate-300 text-sm font-bold hover:bg-primary/20 transition-all">
                                Cancel
                            </button>
                            <button @click="saveCamera"
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
                                    <!-- Video Feed (Real Stream) -->
                                    <div class="aspect-video w-full bg-slate-900 flex items-center justify-center relative group">
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
                                        <video
                                            ref="videoRef"
                                            class="w-full h-full object-cover"
                                            :class="{ 'opacity-0': !isConnected }"
                                            autoplay
                                            muted
                                            playsinline
                                            controls></video>
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
                                            <!-- Existing ROI 1 -->
                                            <polygon fill="rgba(236, 91, 19, 0.2)" points="100,100 400,120 450,300 150,350"
                                                stroke="#ec5b13" stroke-dasharray="8 4" stroke-width="3"></polygon>
                                            <circle cx="100" cy="100" fill="#ec5b13" r="6"></circle>
                                            <circle cx="400" cy="120" fill="#ec5b13" r="6"></circle>
                                            <circle cx="450" cy="300" fill="#ec5b13" r="6"></circle>
                                            <circle cx="150" cy="350" fill="#ec5b13" r="6"></circle>
                                            <text fill="#ec5b13" font-size="14" font-weight="bold" x="110" y="90">Entrance ROI</text>
                                            <!-- Tooltip/Active Point -->
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
                                            <div class="bg-slate-900/80 backdrop-blur-md rounded-lg px-3 py-2 flex items-center gap-2 border border-primary/30 text-[10px] font-bold text-primary uppercase tracking-widest">
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
                                    </div>
                                </div>
                                <div class="flex items-start gap-4 p-4 bg-primary/5 border border-primary/20 rounded-xl shrink-0">
                                    <span class="material-symbols-outlined text-primary">info</span>
                                    <div>
                                        <p class="text-sm font-bold text-slate-900 dark:text-slate-100">ROI Configuration Tip</p>
                                        <p class="text-xs text-slate-600 dark:text-slate-400 mt-1">Drawing specific Regions of Interest (ROI) helps the AI focus on critical areas like entrances or registers, reducing false positives and saving processing power.</p>
                                    </div>
                                </div>
                                <div class="bg-background-light dark:bg-background-dark p-6 rounded-2xl border border-primary/20 shadow-sm flex flex-col gap-6 shrink-0">
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
import { ref, onUnmounted } from 'vue'
import Hls from 'hls.js'
import { MEDIAMTX_URL } from '@/config/api.js'

// --- State ---
const videoRef = ref(null)
const rtspUrl = ref('rtsp://admin:password@192.168.1.104:554/stream')
const isLoading = ref(false)
const isConnected = ref(false)
const errorMsg = ref('')
const cameraName = ref('Camera 1')
let hlsInstance = null

// --- Convert RTSP URL → HLS stream name ---
const getStreamName = (url) => {
  // Encode RTSP URL to safe stream name (base64, no special chars)
  return btoa(url).replace(/[/+=]/g, '_')
}

const getHlsUrl = (url) => {
  const streamName = getStreamName(url)
  return `${MEDIAMTX_URL}/${streamName}/hls.m3u8`
}

// --- Stop current stream ---
const stopStream = () => {
  if (hlsInstance) {
    hlsInstance.destroy()
    hlsInstance = null
  }
  if (videoRef.value) {
    videoRef.value.src = ''
  }
  isConnected.value = false
  isLoading.value = false
  errorMsg.value = ''
}

// --- Connect to RTSP stream via MediaMTX ---
const connectStream = async () => {
  if (!rtspUrl.value.trim()) {
    errorMsg.value = 'Vui lòng nhập RTSP URL'
    return
  }

  stopStream()
  isLoading.value = true
  errorMsg.value = ''

  const hlsUrl = getHlsUrl(rtspUrl.value)

  // Wait for MediaMTX to be ready (it auto-pulls when someone connects via HLS)
  await new Promise(resolve => setTimeout(resolve, 1500))

  // 2. Try native HLS first (Safari)
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
  hlsInstance = new Hls({
    enableWorker: true,
    lowLatencyMode: true,
    backBufferLength: 30,
  })

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

// --- Save camera to localStorage ---
const saveCamera = () => {
  if (!rtspUrl.value.trim() || !cameraName.value.trim()) {
    errorMsg.value = 'Vui lòng nhập đầy đủ thông tin'
    return
  }
  const cameras = JSON.parse(localStorage.getItem('rtsp_cameras') || '[]')
  const id = Date.now()
  cameras.push({ id, name: cameraName.value, rtspUrl: rtspUrl.value })
  localStorage.setItem('rtsp_cameras', JSON.stringify(cameras))
  alert(`Đã lưu camera "${cameraName.value}" thành công!`)
}

// Auto-connect on mount if URL exists
connectStream()

// Cleanup on unmount
onUnmounted(() => {
  stopStream()
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
