# YOS BUS — Git Entry Adapter

**Status:** fallback
**Backend ID:** git
**Versioned:** yes
**Transport commit required:** yes

---

## Role

Git-based BUS entry. Writes packet to Git domain inbox or MPM ready queue, then commits.

This is the **reliable fallback** when no runtime backend is available.

---

## Write Paths

```
01_BACKBONE/BUS/04_DOMAINS/mpm/inbox/{packet_filename}
  OR
01_BACKBONE/MPM/04_QUEUE/ready/{packet_filename}
```

---

## Limitations

- Requires Git commit (slow, ~seconds)
- May trigger GitHub confirmations in ChatGPT context
- Not preferred for high-frequency transport
- Durable: all packets are permanently versioned

---

## bus.py write behavior (git)

```bash
bus.py write --domain mpm --file /path/to/packet.md --backend git
# -> copies to 01_BACKBONE/BUS/04_DOMAINS/mpm/inbox/
# -> git add + commit required separately
```

---

## Notes

Git fallback remains valid and operational. Use when `direct_file` is unavailable.
