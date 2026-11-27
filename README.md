<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <img src="assets/hero-light.svg" width="100%" alt="Hello, I'm Tejas, front-end dev who keeps wandering down the stack: sockets, caches, protocols & C.">
</picture>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-about-dark.svg">
  <img src="assets/h-about-light.svg" width="100%" alt=".about;">
</picture>

Getting straight to the point: I build interfaces for a living, but I don't like working with a black box.

Every abstraction I use eventually makes me curious about the layer underneath it. React led me to the browser's rendering pipeline. `fetch` led me to sockets. "Just use Redis" led me to write a tiny one in C++ to see what it actually does with the bytes.

This profile is where that curiosity lives: small, honest programs written close to the metal, mostly to understand how things *really* work.

And the most important thing: **I use Vim.** Trust me, you should too.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-lowlevel-dark.svg">
  <img src="assets/h-lowlevel-light.svg" width="100%" alt=".under the hood;">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/p-redis-dark.svg">
  <img src="assets/p-redis-light.svg" width="100%" alt="Redis, from scratch — C++, TCP, POSIX sockets, pthreads, binary protocol">
</picture>

A TCP server and client that speak their own **length-prefixed binary protocol**: a 4-byte header carries the message length, then the body follows.

- `read_full` / `write_full` loops, because `read()` and `write()` are allowed to hand you *less* than you asked for.
- Guarding against oversized payloads before they ever touch the buffer.
- Thread-per-connection with `pthread_create` + `pthread_detach`: the simplest concurrency model, so I can feel exactly where it breaks.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/p-lru-dark.svg">
  <img src="assets/p-lru-light.svg" width="100%" alt="LRU cache — C, doubly linked list, manual memory">
</picture>

A least-recently-used cache in plain C. A **doubly linked list** tracks recency (head is fresh, tail is next to go), and a lookup table maps keys to values. On a hit the node moves to the front; when the cache is full the tail gets evicted. No libraries, just `malloc` and pointers.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/p-socket-dark.svg">
  <img src="assets/p-socket-light.svg" width="100%" alt="Talking TCP by hand — C, sockaddr_in, Node.js, Express">
</picture>

A raw C client (`socket` → `connect` → `write` → `read`) talking to a Node.js server, to see what's left once the frameworks are gone: byte order, `sockaddr_in`, and a file descriptor.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/p-brackets-dark.svg">
  <img src="assets/p-brackets-light.svg" width="100%" alt="Bracket checker — C, stack, file I/O">
</picture>

Streams a file one character at a time and validates `()[]{}` nesting with a hand-rolled stack. Written twice: the second version is what I wrote after rereading the first.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-building-dark.svg">
  <img src="assets/h-building-light.svg" width="100%" alt=".building;">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/p-togetherlab-dark.svg">
  <img src="assets/p-togetherlab-light.svg" width="100%" alt="togetherlab — TypeScript, Yjs / CRDTs, WebSockets, PostgreSQL, Redis, Docker">
</picture>

A collaborative workspace where several people edit the same document **in real time**, with live cursors, presence, version history, and recovery after a dropped connection.

The fun part is the system design:

- **CRDTs (Yjs)** so concurrent edits merge without a central lock.
- A **modular monolith** first: auth, workspaces, documents and collaboration stay as separate modules inside one deployable.
- **Redis only when it's earned.** Get one instance right, then scale out and coordinate between instances.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-toolbox-dark.svg">
  <img src="assets/h-toolbox-light.svg" width="100%" alt=".toolbox;">
</picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/l-low-dark.svg"><img src="assets/l-low-light.svg" width="100%" alt="Closer to the metal"></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/chips-low-dark.svg"><img src="assets/chips-low-light.svg" width="100%" alt="C, C++, POSIX sockets, pthreads, Linux, Bash, Vim"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/l-web-dark.svg"><img src="assets/l-web-light.svg" width="100%" alt="The day job stack"></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/chips-web-dark.svg"><img src="assets/chips-web-light.svg" width="100%" alt="TypeScript, JavaScript, React, Next.js, Node.js, Express, TanStack Query, Zustand, Tailwind CSS"></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/l-data-dark.svg"><img src="assets/l-data-light.svg" width="100%" alt="Data & realtime"></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/chips-data-dark.svg"><img src="assets/chips-data-light.svg" width="100%" alt="PostgreSQL, Redis, MongoDB, Prisma, Drizzle, WebSockets"></picture>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-shelf-dark.svg">
  <img src="assets/h-shelf-light.svg" width="100%" alt=".bookshelf;">
</picture>

- **Designing Data-Intensive Applications** by Martin Kleppmann: the book behind most of my "wait, how does *that* work?"
- **Dive into Systems**: C, memory, and the machine underneath it all.
- **Code** by Charles Petzold: from flashlights to CPUs.
- **Network Programming**: sockets, the way the OS sees them.
- **The Pragmatic Programmer**: habits that outlive any framework.
- **Refactoring UI**: because the front-end still has to look good.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-beliefs-dark.svg">
  <img src="assets/h-beliefs-light.svg" width="100%" alt=".beliefs;">
</picture>

> I've never been someone who follows the herd.

Give people a coding agent and every idea starts to look like a nail. I still care about **architecture, code quality, and long-term maintainability**. AI should help us think better and build better software, not replace the part where we think critically and make sound engineering decisions.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-setup-dark.svg">
  <img src="assets/h-setup-light.svg" width="100%" alt=".setup;">
</picture>

- **Arch Linux** with **Sway**, themed Gruvbox end to end: bar, launcher, terminal, cursor.
- **Vim** for everything.
- A `systemd` user service that plays a **sped-up Windows XP startup sound** whenever I plug in the charger. Is it necessary? No. Does it bring me joy every single time? Absolutely.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-hello-dark.svg">
  <img src="assets/h-hello-light.svg" width="100%" alt=".say hello;">
</picture>

Happy to talk about sockets, caches, CRDTs, or why your component re-renders.

<a href="https://tejassharma.in"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/b-portfolio-dark.svg"><img src="assets/b-portfolio-light.svg" alt="Visit my portfolio"></picture></a>&nbsp;&nbsp;<a href="mailto:sharmatejas000@gmail.com"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/b-email-dark.svg"><img src="assets/b-email-light.svg" alt="Say hello"></picture></a>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/divider-dark.svg">
  <img src="assets/divider-light.svg" width="100%" alt="">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg">
  <img src="assets/footer-light.svg" width="100%" alt="{TEJAS} — Code and Design: Me">
</picture>
