# Ping Me API

v2 has no running process. Schema, RLS, Realtime, and Storage live on one Supabase project.

- `legacy/` — diploma Django + Channels + Redis. Interviews only.
- `supabase/migrations/` — source of truth for the live database.

Live frontend: https://ping-me-web-three.vercel.app  
Frontend repo: https://github.com/ShaAnder/ping-me-web

## Rebuild a paused project

1. New Supabase project.
2. Auth → Email on, confirm-email off for demo.
3. SQL editor: run `supabase/migrations/20260912_v2_schema.sql` then `20260912_storage.sql`.
4. Point `ping-me-web` at the new URL + anon key.

Do not put the service-role key in the frontend.
