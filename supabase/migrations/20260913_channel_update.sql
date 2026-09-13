-- Channel rename (v2 addition).
--
-- public.channels had SELECT, INSERT, and DELETE covered, but no UPDATE
-- policy or grant at all. The new per-channel "edit" modal lets the owner
-- rename a channel — without this, that update would silently fail RLS.
-- Scoped the same way as insert/delete: owner of the parent server only.

drop policy if exists "channels_update_owner" on public.channels;
create policy "channels_update_owner"
on public.channels for update to authenticated
using (
  exists (
    select 1 from public.servers s
    where s.id = channels.server_id and s.owner_id = auth.uid()
  )
)
with check (
  exists (
    select 1 from public.servers s
    where s.id = channels.server_id and s.owner_id = auth.uid()
  )
);

grant update on public.channels to authenticated;
