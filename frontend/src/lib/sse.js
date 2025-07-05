export function listenToSSE(onMessage) {
    const eventSource = new EventSource('/api/stream');

    eventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            onMessage(data);
        } catch (err) {
            console.error('Invalid SSE message:', event.data);
        }
    };

    eventSource.onerror = (err) => {
        console.error('SSE error:', err);
        eventSource.close();
    };

    return () => eventSource.close(); // cleanup
}