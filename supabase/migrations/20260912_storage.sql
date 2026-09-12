alter table public.profiles
  add column if not exists avatar_url text,
  add column if not exists bio text,
  add column if not exists location text;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'media',
  'media',
  true,
  2097152,
  array['image/jpeg', 'image/png', 'image/webp', 'image/gif']
)
on conflict (id) do nothing;

create policy "media_public_read"
on storage.objects for select
to public
using (bucket_id = 'media');

create policy "media_auth_insert_own_prefix"
on storage.objects for insert
to authenticated
with check (
  bucket_id = 'media'
  and (
    name like ('avatars/' || auth.uid()::text || '%')
    or name like ('servers/' || auth.uid()::text || '%')
  )
);

create policy "media_auth_update_own_prefix"
on storage.objects for update
to authenticated
using (
  bucket_id = 'media'
  and (
    name like ('avatars/' || auth.uid()::text || '%')
    or name like ('servers/' || auth.uid()::text || '%')
  )
)
with check (
  bucket_id = 'media'
  and (
    name like ('avatars/' || auth.uid()::text || '%')
    or name like ('servers/' || auth.uid()::text || '%')
  )
);

create policy "media_auth_delete_own_prefix"
on storage.objects for delete
to authenticated
using (
  bucket_id = 'media'
  and (
    name like ('avatars/' || auth.uid()::text || '%')
    or name like ('servers/' || auth.uid()::text || '%')
  )
);