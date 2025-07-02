import {
	Box,
	Button,
	Container,
	FormControl,
	Heading,
	Input,
	useToast,
	VStack,
} from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { useParams } from "react-router-dom";
import { createPhoto, getUploadURL, uploadImage } from "../api";
import useHostOnlyPage from "../components/HostOnlyPage";
import ProtectedPage from "../components/ProtectedPage";

interface IForm {
	file: FileList;
}

interface IUploadURLResponse {
	id: string;
	uploadURL: string;
}

// 예시로 ICreatePhotoVariables, ICreatePhotoResponse 를 가정합니다.
interface ICreatePhotoVariables {
	description: string;
	file: string;
	roomPk: string;
}
interface ICreatePhotoResponse {
	ok: boolean;
	// …실제 response shape
}

// 2) uploadImage 훅
interface IUploadImageVariables {
	uploadURL: string;
	file: FileList;
}
interface IUploadImageResponse {
	result: { id: string };
	// …
}

interface IUploadURLResponse {
	uploadURL: string;
}

export default function UploadPhotos() {
	const { register, handleSubmit, watch, reset } = useForm<IForm>();
	const { roomPk } = useParams();
	const toast = useToast();
	const createPhotoMutation = useMutation<
		ICreatePhotoResponse,      // TData: mutate 성공 시 반환 타입
		Error,                     // TError: 실패 시 에러 타입
		ICreatePhotoVariables      // TVariables: mutate 에 넘길 변수의 타입
	>(
		{
			mutationFn: createPhoto,
			onSuccess: () => {
				toast({ status: "success", title: "사진이 업로드되었습니다." });
				reset();
			},
		})

	const uploadImageMutation = useMutation<
		IUploadImageResponse,
		Error,
		IUploadImageVariables
	>({
		mutationFn: uploadImage,
		onSuccess: ({result}) => {
			if (roomPk) {
				createPhotoMutation.mutate({
					description: "I love react",
					file: `https://imagedelivery.net/aSbksvJjax-AUC7qVnaC4A/${result.id}/public`,
					roomPk,
				});
			}
		},
	});

	const uploadURLMutation = useMutation<
		IUploadURLResponse,
		Error,
		void
	>({
		mutationFn: getUploadURL,  // () => Promise<IUploadURLResponse>
		onSuccess: (data) => {
			uploadImageMutation.mutate({
				uploadURL: data.uploadURL,
				file: watch("file"),
			});
		},
	});
	useHostOnlyPage();
	const onSubmit = () => {
		uploadURLMutation.mutate();
	};
	return (
		<ProtectedPage>
			<Box
				pb={40}
				mt={10}
				px={{
					base: 10,
					lg: 40,
				}}
			>
				<Container>
					<Heading textAlign={"center"}>Upload a Photo</Heading>
					<VStack
						as="form"
						onSubmit={handleSubmit(onSubmit)}
						spacing={5}
						mt={10}
					>
						<FormControl>
							<Input {...register("file")} type="file" accept="image/*" />
						</FormControl>
						<Button
							isLoading={
								createPhotoMutation.isPending ||
								uploadImageMutation.isPending ||
								uploadURLMutation.isPending
							}
							type="submit"
							w="full"
							colorScheme={"red"}
						>
							Upload photos
						</Button>
					</VStack>
				</Container>
			</Box>
		</ProtectedPage>
	);
}