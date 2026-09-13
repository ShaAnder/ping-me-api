-- Fix delete cascades for "Delete my account".
--
-- Before this: servers.owner_id was ON DELETE SET NULL (orphans servers
-- instead of removing them) and messages.sender_id was ON DELETE RESTRICT
-- (blocks the user delete outright the moment they've ever sent a message).
-- Both contradict the confirm-dialog copy in DeleteAccountButton.tsx, which
-- already tells the user their servers and messages will be deleted.
--
-- With these as CASCADE: deleting the auth.users row cascades to profiles,
-- which cascades to (a) servers they own -> channels -> messages in those
-- channels, and (b) any messages they sent elsewhere. server_members was
-- already ON DELETE CASCADE on user_id, so membership rows clean up too.

alter table public.servers
  drop constraint if exists servers_owner_id_fkey,
  add constraint servers_owner_id_fkey
    foreign key (owner_id) references public.profiles (id) on delete cascade;

alter table public.messages
  drop constraint if exists messages_sender_id_fkey,
  add constraint messages_sender_id_fkey
    foreign key (sender_id) references public.profiles (id) on delete cascade;