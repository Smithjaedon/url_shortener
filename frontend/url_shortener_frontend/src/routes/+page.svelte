<script>
    import { goto } from '$app/navigation';

    let url = $state('');
    let shortCode = $state('');
    let resultUrl = $state('');
    let shortenError = $state('');
    let shortenLoading = $state(false);
    let copied = $state(false);

    const BASE_URL = 'http://localhost:8000';
    const SHORTEN_ENDPOINT = `${BASE_URL}/urls/shorten/`;

    async function shortenUrl() {
        if (!url.trim()) return;
        shortenError = '';
        resultUrl = '';
        shortenLoading = true;
        try {
            const res = await fetch(SHORTEN_ENDPOINT, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ link: url.trim() })
            });
            if (!res.ok) throw new Error(`Server error: ${res.status}`);
            const data = await res.json();
            shortCode = data.short_link;
            resultUrl = `http://localhost:5173/${shortCode}`;
        } catch (e) {
            shortenError = e.message || 'Something went wrong.';
        } finally {
            shortenLoading = false;
        }
    }

    async function copyToClipboard() {
        try {
            await navigator.clipboard.writeText(resultUrl);
            copied = true;
            setTimeout(() => (copied = false), 2000);
        } catch {}
    }
</script>

<svelte:head>
    <title>Snip — URL Shortener</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="" />
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Fraunces:ital,opsz,wght@0,9..144,300;1,9..144,300&display=swap" rel="stylesheet" />
</svelte:head>

<main class="min-h-screen bg-[#0e0e10] text-[#e8e6df] flex flex-col items-center justify-center px-5 py-12 gap-6" style="font-family: 'DM Mono', monospace;">

    <!-- Header -->
    <header class="text-center mb-2">
        <div class="flex items-center justify-center gap-2 mb-1">
            <span class="text-[#c9a86c] text-xl">✦</span>
            <span class="text-[#f0ede4] text-4xl font-light tracking-tight" style="font-family: 'Fraunces', serif; font-style: italic;">snip</span>
        </div>
        <p class="text-[#6b6860] text-[11px] tracking-[0.12em] uppercase">Long URLs, made short.</p>
    </header>

    <!-- Shorten card -->
    <section class="w-full max-w-[560px] bg-[#17171a] border border-[#2e2d2b] rounded-2xl p-7 flex flex-col gap-4">
        <span class="text-[#6b6860] text-[11px] tracking-[0.12em] uppercase">Shorten a URL</span>

        <div class="flex gap-2.5">
            <input
                    type="text"
                    bind:value={url}
                    onkeydown={(e) => e.key === 'Enter' && shortenUrl()}
                    placeholder="https://your-very-long-url.com/goes/here"
                    autocomplete="off"
                    spellcheck="false"
                    class="flex-1 min-w-0 bg-[#0e0e10] border border-[#2e2d2b] rounded-lg px-3.5 py-2.5 text-[#e8e6df] text-[13px] placeholder-[#3d3c3a] outline-none focus:border-[#c9a86c] transition-colors"
                    style="font-family: 'DM Mono', monospace;"
            />
            <button
                    onclick={shortenUrl}
                    disabled={shortenLoading || !url.trim()}
                    class="flex items-center gap-1.5 px-5 py-2.5 bg-[#c9a86c] text-[#0e0e10] rounded-lg text-[12px] font-medium tracking-wider whitespace-nowrap transition-opacity hover:opacity-80 active:scale-95 disabled:opacity-30 disabled:cursor-not-allowed"
                    style="font-family: 'DM Mono', monospace;"
            >
                {#if shortenLoading}
                    <span class="w-3 h-3 border border-[#0e0e10] border-t-transparent rounded-full animate-spin"></span>
                {:else}
                    Shorten
                {/if}
            </button>
        </div>

        {#if shortenError}
            <p class="text-[#c0524e] text-[12px]">{shortenError}</p>
        {/if}

        {#if resultUrl}
            <div class="bg-[#0e0e10] border border-[#2e2d2b] rounded-lg px-4 py-3.5 flex flex-col gap-1.5">
                <div class="flex items-center gap-3">
                    <a
                            href={resultUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            class="flex-1 min-w-0 text-[#c9a86c] text-[13px] truncate hover:underline"
                    >{resultUrl}</a>
                    <button
                            onclick={copyToClipboard}
                            class="flex-shrink-0 flex items-center gap-1.5 bg-[#1e1e21] border border-[#2e2d2b] rounded-md px-2.5 py-1.5 text-[#8a8880] text-[11px] hover:text-[#c9a86c] hover:border-[#c9a86c] transition-colors"
                            style="font-family: 'DM Mono', monospace;"
                    >
                        {#if copied}
                            <svg width="13" height="13" viewBox="0 0 16 16" fill="none"><path d="M3 8l3.5 3.5L13 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                            Copied!
                        {:else}
                            <svg width="13" height="13" viewBox="0 0 16 16" fill="none"><rect x="5" y="5" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.3"/><path d="M3 11V3h8" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
                            Copy
                        {/if}
                    </button>
                </div>
                <span class="text-[#4a4947] text-[11px]">Code: <code class="text-[#6b6860]">{shortCode}</code></span>
            </div>
        {/if}
    </section>

</main>