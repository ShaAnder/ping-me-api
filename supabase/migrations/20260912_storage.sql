-- Ping Me v2 — Storage bucket + RLS
-- Paths: avatars/{userId}.ext  servers/{serverId}/icon.ext|banner.ext

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'media',
  'media',
  true,
  10485760,
  array['image/jpeg', 'image/png', 'image/webp', 'image/gif']
)
on conflict (id) do update
set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "media_public_read" on storage.objects;
drop policy if exists "media_auth_write" on storage.objects;
drop policy if exists "media_auth_update" on storage.objects;
drop policy if exists "media_auth_delete" on storage.objects;
drop policy if exists "media_auth_insert_own_prefix" on storage.objects;
drop policy if exists "media_auth_update_own_prefix" on storage.objects;
drop policy if exists "media_auth_delete_own_prefix" on storage.objects;

create policy "media_public_read"
on storage.objects for select
to public
using (bucket_id = 'media');

create policy "media_auth_write"
on storage.objects for insert
to authenticated
with check (
  bucket_id = 'media'
  and (
    storage.objects.name like ('avatars/' || auth.uid()::text || '%')
    or exists (
      select 1 from public.servers s
      where s.owner_id = auth.uid()
        and storage.objects.name like ('servers/' || s.id::text || '/%')
    )
  )
);

create policy "media_auth_update"
on storage.objects for update
to authenticated
using (
  bucket_id = 'media'
  and (
    storage.objects.name like ('avatars/' || auth.uid()::text || '%')
    or exists (
      select 1 from public.servers s
      where s.owner_id = auth.uid()
        and storage.objects.name like ('servers/' || s.id::text || '/%')
    )
  )
)
with check (
  bucket_id = 'media'
  and (
    storage.objects.name like ('avatars/' || auth.uid()::text || '%')
    or exists (
      select 1 from public.servers s
      where s.owner_id = auth.uid()
        and storage.objects.name like ('servers/' || s.id::text || '/%')
    )
  )
);

create policy "media_auth_delete"
on storage.objects for delete
to authenticated
using (
  bucket_id = 'media'
  and (
    storage.objects.name like ('avatars/' || auth.uid()::text || '%')
    or exists (
      select 1 from public.servers s
      where s.owner_id = auth.uid()
        and storage.objects.name like ('servers/' || s.id::text || '/%')
    )
  )
);