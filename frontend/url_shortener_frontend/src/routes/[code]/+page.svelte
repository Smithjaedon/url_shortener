<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    const BASE_URL = 'http://localhost:8000';
    let error = $state('');

    onMount(async () => {
        const code = $page.params.code;
        try {
            const res = await fetch(`${BASE_URL}/urls/${code}/`);
            if (!res.ok) throw new Error(res.status === 404 ? 'Short link not found.' : `Server error: ${res.status}`);
            const data = await res.json();
            window.location.href = data.redirect_link;
        } catch (e) {
            error = e.message || 'Something went wrong.';
        }
    });
</script>

<svelte:head>
    <title>Redirecting…</title>
</svelte:head>

<main class="min-h-screen bg-[#0e0e10] text-[#e8e6df] flex flex-col items-center justify-center"
      style="font-family: 'DM Mono', monospace;">
    {#if error}
        <p class="text-[#c0524e] text-[13px] mb-4">{error}</p>
        <a href="/" class="text-[#c9a86c] text-[12px] hover:underline">← Back to Snip</a>
    {:else}
        <p class="text-[#6b6860] text-[12px] tracking-widest uppercase">Redirecting…</p>
    {/if}
</main>