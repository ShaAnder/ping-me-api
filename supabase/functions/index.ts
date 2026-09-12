// // supabase/functions/delete-user/index.ts
// //
// // Deletes the calling user's own account. Deploy with:
// //   supabase functions deploy delete-user
// //
// // SUPABASE_URL, SUPABASE_ANON_KEY and SUPABASE_SERVICE_ROLE_KEY are injected
// // automatically into every Edge Function's environment — no secrets to set
// // manually for this one.

// import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

// const corsHeaders = {
// 	"Access-Control-Allow-Origin": "*",
// 	"Access-Control-Allow-Headers":
// 		"authorization, x-client-info, apikey, content-type",
// };

// Deno.serve(async (req: Request) => {
// 	if (req.method === "OPTIONS") {
// 		return new Response("ok", { headers: corsHeaders });
// 	}

// 	try {
// 		const authHeader = req.headers.get("Authorization");
// 		if (!authHeader) {
// 			return new Response(
// 				JSON.stringify({ error: "Missing Authorization header" }),
// 				{
// 					status: 401,
// 					headers: { ...corsHeaders, "Content-Type": "application/json" },
// 				},
// 			);
// 		}

// 		// Scoped to the caller's own JWT — only used to find out who's asking.
// 		const supabaseClient = createClient(
// 			Deno.env.get("SUPABASE_URL")!,
// 			Deno.env.get("SUPABASE_ANON_KEY")!,
// 			{ global: { headers: { Authorization: authHeader } } },
// 		);

// 		const {
// 			data: { user },
// 			error: userError,
// 		} = await supabaseClient.auth.getUser();

// 		if (userError || !user) {
// 			return new Response(
// 				JSON.stringify({ error: "Invalid or expired session" }),
// 				{
// 					status: 401,
// 					headers: { ...corsHeaders, "Content-Type": "application/json" },
// 				},
// 			);
// 		}

// 		// Service-role client — the only one allowed to call the admin API.
// 		// Never expose SUPABASE_SERVICE_ROLE_KEY to the frontend; it only
// 		// exists inside this function's server-side environment.
// 		const supabaseAdmin = createClient(
// 			Deno.env.get("SUPABASE_URL")!,
// 			Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
// 		);

// 		const { error: deleteError } = await supabaseAdmin.auth.admin.deleteUser(
// 			user.id,
// 		);

// 		if (deleteError) {
// 			return new Response(JSON.stringify({ error: deleteError.message }), {
// 				status: 500,
// 				headers: { ...corsHeaders, "Content-Type": "application/json" },
// 			});
// 		}

// 		return new Response(JSON.stringify({ success: true }), {
// 			status: 200,
// 			headers: { ...corsHeaders, "Content-Type": "application/json" },
// 		});
// 	} catch (err) {
// 		return new Response(JSON.stringify({ error: (err as Error).message }), {
// 			status: 500,
// 			headers: { ...corsHeaders, "Content-Type": "application/json" },
// 		});
// 	}
// });
