-- Delete channel (v1 parity).
--
-- public.channels had a SELECT policy and grant only. There was no DELETE
-- (or INSERT) policy/grant at all, so MessageInterface.tsx's delete-channel
-- button was wired to nothing more than closing its own modal and
-- navigating away — the row was never actually removed. AddChannel.tsx
-- inserting channels was similarly relying on nothing but frontend gating
-- (isOwner prop) with no DB-level enforcement behind it.
--
-- Both are scoped to "you own the server this channel belongs to", matching
-- the isOwner gating already used in the frontend for both actions.

drop policy if exists "channels_insert_owner" on public.channels;
create policy "channels_insert_owner"
on public.channels for insert to authenticated
with check (
  exists (
    select 1 from public.servers s
    where s.id = channels.server_id and s.owner_id = auth.uid()
  )
);

drop policy if exists "channels_delete_owner" on public.channels;
create policy "channels_delete_owner"
on public.channels for delete to authenticated
using (
  exists (
    select 1 from public.servers s
    where s.id = channels.server_id and s.owner_id = auth.uid()
  )
);

grant insert, delete on public.channels to authenticated;