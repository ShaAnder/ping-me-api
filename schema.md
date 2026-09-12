```sql

-- ping-me slice schema
-- persist first (client INSERT/UPDATE/DELETE on messages)
-- live fanout = Realtime postgres_changes on messages
-- late joiners = SELECT, not socket backlog

create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  username text not null,
  created_at timestamptz not null default now(),
  constraint profiles_username_len check (char_length(username) between 2 and 32)
);

create table public.servers (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  description text,
  owner_id uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now()
);

create table public.channels (
  id uuid primary key default gen_random_uuid(),
  server_id uuid not null references public.servers (id) on delete cascade,
  name text not null,
  created_at timestamptz not null default now()
);

create table public.server_members (
  server_id uuid not null references public.servers (id) on delete cascade,
  user_id uuid not null references public.profiles (id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (server_id, user_id)
);

create table public.messages (
  id uuid primary key default gen_random_uuid(),
  channel_id uuid not null references public.channels (id) on delete cascade,
  sender_id uuid not null references public.profiles (id) on delete restrict,
  content text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint messages_content_len check (char_length(content) between 1 and 2000)
);

create index messages_channel_created_idx
  on public.messages (channel_id, created_at);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger messages_set_updated_at
before update on public.messages
for each row
execute function public.set_updated_at();

-- New signup -> profile + membership on the seeded server
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  seed_server uuid;
  uname text;
begin
  uname := coalesce(
    nullif(new.raw_user_meta_data->>'username', ''),
    split_part(new.email, '@', 1)
  );

  insert into public.profiles (id, username)
  values (new.id, uname);

  select id into seed_server
  from public.servers
  where name = 'Ping Me'
  limit 1;

  if seed_server is not null then
    insert into public.server_members (server_id, user_id)
    values (seed_server, new.id)
    on conflict do nothing;
  end if;

  return new;
end;
$$;

create trigger on_auth_user_created
after insert on auth.users
for each row
execute function public.handle_new_user();

-- Seed: one server, one room
insert into public.servers (name, description)
values ('Ping Me', 'The live room');

insert into public.channels (server_id, name)
select id, 'general'
from public.servers
where name = 'Ping Me'
limit 1;

alter table public.profiles enable row level security;
alter table public.servers enable row level security;
alter table public.channels enable row level security;
alter table public.server_members enable row level security;
alter table public.messages enable row level security;

create policy "profiles_select_authenticated"
on public.profiles for select
to authenticated
using (true);

create policy "profiles_update_own"
on public.profiles for update
to authenticated
using (id = auth.uid())
with check (id = auth.uid());

create policy "servers_select_member"
on public.servers for select
to authenticated
using (
  exists (
    select 1 from public.server_members m
    where m.server_id = servers.id
      and m.user_id = auth.uid()
  )
);

create policy "channels_select_member"
on public.channels for select
to authenticated
using (
  exists (
    select 1 from public.server_members m
    where m.server_id = channels.server_id
      and m.user_id = auth.uid()
  )
);

create policy "members_select_own_rows"
on public.server_members for select
to authenticated
using (user_id = auth.uid());

create policy "messages_select_member"
on public.messages for select
to authenticated
using (
  exists (
    select 1
    from public.channels c
    join public.server_members m on m.server_id = c.server_id
    where c.id = messages.channel_id
      and m.user_id = auth.uid()
  )
);

create policy "messages_insert_member"
on public.messages for insert
to authenticated
with check (
  sender_id = auth.uid()
  and exists (
    select 1
    from public.channels c
    join public.server_members m on m.server_id = c.server_id
    where c.id = messages.channel_id
      and m.user_id = auth.uid()
  )
);

create policy "messages_update_own"
on public.messages for update
to authenticated
using (sender_id = auth.uid())
with check (sender_id = auth.uid());

create policy "messages_delete_own"
on public.messages for delete
to authenticated
using (sender_id = auth.uid());

-- Realtime: edit/delete payloads need the old row
alter table public.messages replica identity full;

alter publication supabase_realtime add table public.messages;

grant usage on schema public to authenticated;
grant select on public.profiles, public.servers, public.channels, public.server_members to authenticated;
grant select, insert, update, delete on public.messages to authenticated;
grant update on public.profiles to authenticated;

```
